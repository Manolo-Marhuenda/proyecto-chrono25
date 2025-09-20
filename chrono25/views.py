from django.shortcuts import render,redirect, get_object_or_404

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views import View
from decimal import Decimal
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from profiles.models import UserProfile
from django.views.generic import ListView
from django.conf import settings
from django.core.mail import send_mail
from reloj.models import Reloj
from .forms import RegistrationForm, LoginForm, ContactoForm
from django.views.generic.edit import FormView
from django.views.generic import DetailView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import OrdenDeCompra
from orderItem.models import ItemDeOrden




class HomeView(ListView):
    template_name = 'general/home.html'
    model = Reloj
    context_object_name = 'relojes' # Nombre para acceder a la lista en la plantilla
    paginate_by = 10 # Número de elementos por página

    def get_queryset(self):
        # Devuelve solo los relojes que no se han vendido
        return Reloj.objects.filter(vendido=False)


class LoginView(FormView):
    template_name = 'general/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        usuario = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=usuario, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f'Bienvenido de nuevo {user.username}')
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            messages.add_message(self.request, messages.ERROR, 'Usuario o contraseña incorrectos')
            return super(LoginView, self).form_invalid(form)



class RegisterView(CreateView):
    template_name = 'general/register.html'
    model = User
    success_url = reverse_lazy('login')
    form_class = RegistrationForm

    def form_valid(self, form):
        user = form.save()
        messages.add_message(self.request, messages.SUCCESS, "Usuario creado correctamente.")
        return super(RegisterView,self).form_valid(form)
    


def contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Aquí va la lógica para procesar el formulario
             # Obtener los datos del formulario
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            mensaje = form.cleaned_data['mensaje']

            # Construir el asunto y el cuerpo del correo
            asunto = f'Mensaje de contacto de {nombre}'
            cuerpo = f'De: {nombre} <{correo}>\n\n{mensaje}'
            
            # Dirección de correo a la que se enviará el mensaje
            destinatario = settings.EMAIL_HOST_USER # O cualquier otra dirección

            # Enviar el correo
            send_mail(
                asunto,
                cuerpo,
                settings.EMAIL_HOST_USER, # Remitente
                [destinatario], # Lista de destinatarios
                fail_silently=False,
            )
            messages.add_message(request, messages.SUCCESS, "Email enviado correctamente.")
            return HttpResponseRedirect(reverse_lazy('home'))  # Redirige a una página de éxito
    else:
        form = ContactoForm()
    
    return render(request, "general/contact.html", {"form": form})


class LegaltView(TemplateView):
    template_name = 'general/legal.html'


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    template_name = 'general/profile_detail.html'
    model = UserProfile
    context_object_name = 'profile'


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    template_name = 'general/profile_update.html'
    model = UserProfile
    context_object_name = 'profile'
    fields = ['pais', 'profile_picture']

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().user.pk:
            messages.add_message(request, messages.ERROR, 'No tienes permiso para editar este perfil.')
            return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.add_message(self.request, messages.SUCCESS, "Perfil actualizado correctamente.")
        return super(ProfileUpdateView,self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'pk': self.object.pk})

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Has cerrado sesión correctamente.')
    return HttpResponseRedirect(reverse_lazy('home'))


class CarritoView(TemplateView):
    template_name = 'carrito/ver_carrito_cbv.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # El objeto 'request' se accede a través de self.request en TemplateView
        carrito_ids = self.request.session.get('carrito', [])
        
        items_carrito = []
        total_carrito = Decimal('0.00')

        for reloj_id in carrito_ids:
            reloj = get_object_or_404(Reloj, pk=reloj_id)
            subtotal = reloj.price
            total_carrito += subtotal
            items_carrito.append({
                'reloj': reloj,
                'subtotal': subtotal
            })
        
        context['items_carrito'] = items_carrito
        context['total_carrito'] = total_carrito
        
        return context


class AgregarAlCarritoView(View):
    def post(self, request, reloj_id, *args, **kwargs):
        carrito = request.session.get('carrito', [])

        if not isinstance(carrito, list):
            carrito = []
        
        # Solo agregamos el reloj si no está ya en el carrito
        if reloj_id not in carrito:
            carrito.append(reloj_id)
        
        request.session['carrito'] = carrito
        return redirect('ver_carrito_cbv')



class EliminarDelCarritoView(View):
    def post(self, request, reloj_id, *args, **kwargs):
        carrito = request.session.get('carrito', [])
        
        if reloj_id in carrito:
            carrito.remove(reloj_id)
        
        request.session['carrito'] = carrito
        return redirect('ver_carrito_cbv')



class CrearOrdenCompraView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        carrito_ids = request.session.get('carrito', [])
        if not carrito_ids:
            return redirect('ver_carrito_cbv')

        # Crear la Orden de Compra
        orden = OrdenDeCompra.objects.create(
            cliente=request.user,
            completada=True,
        )

        # Crear los ítems de la orden y marcar los relojes como vendidos
        for reloj_id in carrito_ids:
            reloj = get_object_or_404(Reloj, pk=reloj_id)
            
            # Solo si el reloj no ha sido vendido por otro cliente
            if not reloj.vendido:
                ItemDeOrden.objects.create(
                    orden=orden,
                    reloj=reloj,
                )
                
                # Marcar el reloj como vendido para que "desaparezca"
                reloj.vendido = True
                reloj.save()

        # Limpiar el carrito de la sesión
        request.session['carrito'] = []

        return render(request, 'carrito/orden_creada.html', {'orden': orden})
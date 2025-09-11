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
from reloj.models import Reloj
from .forms import RegistrationForm, LoginForm
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
    


class ContactView(TemplateView):
    template_name = 'general/contact.html'


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
        carrito = self.request.session.get('carrito', {})
        items_carrito = []
        total_carrito = Decimal('0.00')

        for reloj_id, cantidad in carrito.items():
            try:
                reloj = get_object_or_404(Reloj, pk=reloj_id)
                subtotal = reloj.precio * cantidad
                total_carrito += subtotal
                items_carrito.append({
                    'reloj': reloj,
                    'cantidad': cantidad,
                    'subtotal': subtotal
                })
            except ValueError:
                # Manejar el caso donde reloj_id no es un entero válido
                continue

        context['items_carrito'] = items_carrito
        context['total_carrito'] = total_carrito
        return context


class AgregarAlCarritoView(View):
    def post(self, request, reloj_id, *args, **kwargs):
        reloj = get_object_or_404(Reloj, pk=reloj_id)
        carrito = request.session.get('carrito', {})
        
        reloj_id_str = str(reloj.id)
        if reloj_id_str in carrito:
            carrito[reloj_id_str] += 1
        else:
            carrito[reloj_id_str] = 1
        
        request.session['carrito'] = carrito
        return redirect('ver_carrito_cbv')



class EliminarDelCarritoView(View):
    def post(self, request, reloj_id, *args, **kwargs):
        carrito = request.session.get('carrito', {})
        reloj_id_str = str(reloj_id)
        if reloj_id_str in carrito:
            del carrito[reloj_id_str]
            request.session['carrito'] = carrito
        return redirect('ver_carrito_cbv')



class CrearOrdenCompraView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        carrito = request.session.get('carrito', {})
        if not carrito:
            return redirect('ver_carrito_cbv')

        # Crear la Orden de Compra
        orden = OrdenDeCompra.objects.create(
            cliente=request.user,
            completada=True
        )

        # Crear los Ítems de la Orden
        for reloj_id, cantidad in carrito.items():
            reloj = get_object_or_404(Reloj, pk=reloj_id)
            ItemDeOrden.objects.create(
                orden=orden,
                reloj=reloj,
                cantidad=cantidad
            )
        
        # Limpiar el carrito de la sesión
        request.session['carrito'] = {}

        return render(request, 'orden_creada.html', {'orden': orden})
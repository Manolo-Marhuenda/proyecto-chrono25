from django.shortcuts import render
from django.views.generic import TemplateView, View, CreateView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ValoracionForm
from .models import Valoracion

from orden.models import Order, OrderItem
from product.models import Product
from django.shortcuts import redirect, get_object_or_404

# Create your views here.
class VerCarritoView(TemplateView):
    template_name = 'orden/carrito.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrito_ids = self.request.session.get('carrito', [])
        
        # Obtenemos los objetos Reloj de la BD
        relojes = Product.objects.filter(id__in=carrito_ids)
        
        context['relojes'] = relojes
        context['total'] = sum(reloj.price for reloj in relojes)
        return context


class AgregarAlCarritoView(View):
    # Solo implementamos post(), sin plantilla ni get()
    def post(self, request, reloj_id):
        reloj = get_object_or_404(Product, id=reloj_id)
        carrito = request.session.get('carrito', [])
        reloj_id_str = str(reloj.id)
        if reloj_id_str not in carrito:
            carrito.append(reloj_id_str)
            request.session['carrito'] = carrito
            request.session.modified = True

        return redirect('ver_carrito')


class EliminarDelCarritoView(View):
    def post(self, request, reloj_id):
        # 1. Convertimos el ID a string (como los guardamos en la sesión)
        reloj_id_str = str(reloj_id)
        
        # 2. Obtenemos la lista actual del carrito de la sesión
        carrito = request.session.get('carrito', [])

        # 3. Si el reloj está en la lista, lo eliminamos
        if reloj_id_str in carrito:
            carrito.remove(reloj_id_str)
            
            # Guardamos la lista actualizada de vuelta en la sesión
            request.session['carrito'] = carrito
            request.session.modified = True

        # 4. Redirigimos de vuelta a la vista del carrito
        return redirect('ver_carrito')


class CheckoutView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['direccion']  # El usuario solo rellena la dirección de envío
    template_name = 'orden/checkout.html'
    success_url = reverse_lazy('home')  

    def dispatch(self, request, *args, **kwargs):
        # Si el carrito en la sesión está vacío, no permitimos entrar al checkout
        carrito_ids = request.session.get('carrito', [])
        if not carrito_ids:
            return redirect('ver_carrito')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # 1. Asignamos el usuario actual y el estado inicial a 'P' (Pendiente)
        form.instance.user = self.request.user
        form.instance.estado = 'P'

        # Obtenemos los IDs de la sesión
        carrito_ids = self.request.session.get('carrito', [])
        
        # Filtramos los productos disponibles que no hayan sido vendidos previamente
        productos = Product.objects.filter(id__in=carrito_ids, is_sold=False)

        if not productos.exists():
            # Si ningún producto está disponible, redirigimos al carrito
            return redirect('ver_carrito')

        # 2. Usamos transaction.atomic para asegurar que todo se guarde o nada si hay error
        with transaction.atomic():
            # Guardamos la instancia del objeto Order en la BD
            response = super().form_valid(form)

            # 3. Trasladamos los relojes de la sesión a registros OrderItem
            for product in productos:
                OrderItem.objects.create(
                    order=self.object,           # self.object es la Order recién creada
                    product=product,
                    price=product.price  # Congelamos el precio de venta
                )
                
                # 4. Marcamos el reloj como vendido para retirarlo del catálogo
                product.is_sold = True
                product.save()

            # 5. Vaciamos el carrito de la sesión
            self.request.session['carrito'] = []
            self.request.session.modified = True
            messages.add_message(self.request, messages.SUCCESS, 'Pedido realizado con éxito.')

        return response


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orden/order_list.html'
    context_object_name = 'ordenes'

    def get_queryset(self):
        # Filtramos las órdenes para que solo se muestren las del usuario actual
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class ValorarOrdenView(LoginRequiredMixin, CreateView):
    model = Valoracion
    form_class = ValoracionForm
    template_name = 'orden/valorar_orden.html'
    success_url = reverse_lazy('order_list')

    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, pk=self.kwargs['order_id'])

        # Validar que el pedido pertenezca al usuario conectado
        if self.order.user != request.user:
            messages.error(request, "No tienes permiso para acceder a este pedido.")
            return redirect('order_list')

        # Obtenemos el vendedor del primer reloj del pedido (o ajusta si hay múltiples)
        primer_item = self.order.items.first()
        self.vendedor = primer_item.product.vendedor if primer_item else None

        if not self.vendedor:
            messages.error(request, "No se encontró el vendedor asociado a este pedido.")
            return redirect('order_list')

        # Comprobar si ya existe valoración para esta orden y este vendedor
        if Valoracion.objects.filter(order=self.order, vendedor=self.vendedor).exists():
            messages.warning(request, "Ya has enviado una valoración para este pedido.")
            return redirect('order_list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.order = self.order
        form.instance.comprador = self.request.user
        form.instance.vendedor = self.vendedor
        # 1  Guardamos la instancia de la Valoración en la base de datos.
        response = super().form_valid(form)
        # 2. ACTUALIZAMOS EL USERPROFILE DEL VENDEDOR
        # self.object contiene el objeto Valoracion recién guardado
        self.vendedor.profile.agregar_valoracion(self.object.puntuacion)
        messages.success(self.request, "¡Gracias! Tu valoración ha sido registrada.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        context['vendedor'] = self.vendedor
        return context
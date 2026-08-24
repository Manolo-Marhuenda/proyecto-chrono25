from django.shortcuts import render
from django.views.generic import TemplateView, View, CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

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
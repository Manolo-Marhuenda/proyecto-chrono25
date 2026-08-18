from django.contrib import messages
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(login_required, name='dispatch')
class CreateProductView(CreateView):
    model = Product
    template_name = 'product/create_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Asignar el usuario actual como vendedor antes de guardar
        form.instance.vendedor = self.request.user
        messages.add_message(self.request, messages.SUCCESS, 'Reloj Puesto a la venta exitosamente. Ahora puedes verlo en tu perfil.')
        return super().form_valid(form)

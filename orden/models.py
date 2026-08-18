from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.
class Order(models.Model):
    ESTADOS = [
        ('P', 'Pendiente'),
        ('E', 'Enviado'),
        ('C', 'Completado'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordenes')
    direccion = models.CharField(max_length=255)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} de {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def save(self, *args, **kwargs):
        # Toma automáticamente el precio del reloj si no se indica uno
        if self.price is None and self.product:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.marca} (Pedido #{self.order.id})"
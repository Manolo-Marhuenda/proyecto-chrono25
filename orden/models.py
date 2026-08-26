from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

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


class Valoracion(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='valoraciones'
    )
    vendedor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='valoraciones_recibidas'
    )
    comprador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='valoraciones_realizadas'
    )
    # La puntuación debe estar entre 1 y 5 y se valida automáticamente
    puntuacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Valoración"
        verbose_name_plural = "Valoraciones"
        ordering = ['-created_at']
        # Garantiza que solo exista 1 valoración por vendedor dentro del mismo pedido
        unique_together = ('order', 'vendedor')

    def __str__(self):
        return f"Pedido #{self.order.id} | {self.comprador.username} -> {self.vendedor.username} ({self.puntuacion}★)"
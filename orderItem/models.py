from django.db import models
from reloj.models import Reloj
from order.models import OrdenDeCompra

# Create your models here.
class ItemDeOrden(models.Model):
    reloj = models.ForeignKey(Reloj, on_delete=models.CASCADE)
    orden = models.ForeignKey(OrdenDeCompra, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def get_total_item(self):
        # Calcula el precio total de este ítem (precio del reloj * cantidad)
        return self.reloj.precio * self.cantidad
    
    def __str__(self):
        return f"{self.cantidad} x {self.reloj.nombre} en la Orden #{self.orden.id}"
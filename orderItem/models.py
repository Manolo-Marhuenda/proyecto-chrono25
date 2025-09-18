from django.db import models
from reloj.models import Reloj
from order.models import OrdenDeCompra
from django.contrib.auth.models import User

# Create your models here.
class ItemDeOrden(models.Model):
    reloj = models.ForeignKey(Reloj, on_delete=models.CASCADE)
    orden = models.ForeignKey(OrdenDeCompra, on_delete=models.CASCADE)

    def get_total_item(self):
        # Calcula el precio total de este ítem (precio del reloj * cantidad)
        return self.reloj.price 
    
    def __str__(self):
        return f"{self.reloj.marca} en la Orden #{self.orden.id}"
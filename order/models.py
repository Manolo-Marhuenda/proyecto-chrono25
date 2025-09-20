from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class OrdenDeCompra(models.Model):

    METODOS_PAGO_CHOICES = [
        ('contado', 'Contado'),
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_orden = models.DateTimeField(auto_now_add=True)
    completada = models.BooleanField(default=False)
    direccion_envio = models.CharField(max_length=255, blank=True, null=True)
    metodo_pago = models.CharField(max_length=20,choices=METODOS_PAGO_CHOICES,)
    

    def get_total_orden(self):
        # Calcula el precio total de todos los ítems en esta orden
        items = self.itemdeorden_set.all()
        total = sum([item.get_total_item() for item in items])
        return total

    def __str__(self):
        return f"Orden #{self.id} de {self.cliente.username}"
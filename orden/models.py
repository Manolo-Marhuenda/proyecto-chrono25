from django.db import models
from django.contrib.auth.models import User

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
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Reloj(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Usuario')
    marca = models.CharField(max_length=100) # Manual para en un futuro hacer un desplegable.
    modelo = models.CharField(max_length=100) # Manual para en un futuro hacer un desplegable segun marca.
    image= models.ImageField(upload_to='reloj_images/', verbose_name='Imagen')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reloj'
        verbose_name_plural = 'Relojes'

    def __str__(self):
        return self.marca + ' ' + self.modelo

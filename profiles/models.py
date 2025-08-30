from django.db import models
from django.contrib.auth.models import User
from .choices import COUNTRIES

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    pais = models.CharField(max_length=2, choices=COUNTRIES, default='ES', verbose_name='País',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de alta')
    profile_picture = models.ImageField('Imagen de perfil', upload_to='profile_pictures/', blank=True, null=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        
    def __str__(self):
        return f'Perfil de {self.user.username}'
    


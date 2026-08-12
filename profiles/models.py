from django.db import models

# Create your models here.
# este modelo es para crear un perfil de usuario extendido, 
# que se vincula con el modelo User de Django mediante una relación uno a uno. 
# Esto permite almacenar información adicional sobre el usuario, 
# como su foto de perfil y su biografía.
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField('Imagen de perfil', upload_to='profile_photos/', blank=True, null=True)
    biography = models.TextField(max_length=200, blank=True, null=True)
    #para poder valorar a los usuarios, se añade un campo de valoración con opciones predefinidas.
    OPCIONES_VALORACION = [
        (1, '⭐ (1/5) - Muy malo'),
        (2, '⭐⭐ (2/5) - Regular'),
        (3, '⭐⭐⭐ (3/5) - Bueno'),
        (4, '⭐⭐⭐⭐ (4/5) - Muy bueno'),
        (5, '⭐⭐⭐⭐⭐ (5/5) - Excelente'),
    ]
    valoracion = models.IntegerField(
        choices=OPCIONES_VALORACION,
        default=5,
        verbose_name="Valoración"
    )
    def __str__(self):
        return f"Perfil de {self.user.username} con valoración de {self.valoracion} estrellas"
    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"


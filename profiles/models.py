from django.db import models
from django.db.models import Avg

# Create your models here.
# este modelo es para crear un perfil de usuario extendido, 
# que se vincula con el modelo User de Django mediante una relación uno a uno. 
# Esto permite almacenar información adicional sobre el usuario, 
# como su foto de perfil y su biografía.
from django.contrib.auth.models import User
from orden.models import Order
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField('Imagen de perfil', upload_to='profile_photos/', blank=True, null=True)
    biography = models.TextField(max_length=200, blank=True, null=True)

    rating_medio = models.FloatField(
        'Valoración media',
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    total_valoraciones = models.PositiveIntegerField(
        'Total de valoraciones',
        default=0
    )

    def __str__(self):
        return f"Perfil de {self.user}"

    def agregar_valoracion(self, nueva_puntuacion):
        """
        Recibe un número de 1 a 5, recalcula la media acumulada
        y guarda los cambios en la base de datos.
        """
        puntos_actuales = self.rating_medio * self.total_valoraciones
        self.total_valoraciones += 1
        self.rating_medio = round((puntos_actuales + nueva_puntuacion) / self.total_valoraciones, 1)
        self.save()
from django.db import models
from django.db.models import Avg

# Create your models here.
# este modelo es para crear un perfil de usuario extendido, 
# que se vincula con el modelo User de Django mediante una relación uno a uno. 
# Esto permite almacenar información adicional sobre el usuario, 
# como su foto de perfil y su biografía.
from django.contrib.auth.models import User
from orden.models import Order


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField('Imagen de perfil', upload_to='profile_photos/', blank=True, null=True)
    biography = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user}"

"""     # MÉTODO QUE CALCULA LA MEDIA EN TIEMPO REAL
    @property
    def media_valoracion(self):
        
        #Calcula la media de las puntuaciones recibidas.
        #Si nadie lo ha valorado aún, devuelve 0.0 (o el valor inicial que prefieras).
        
        resultado = self.ratings_recibidos.aggregate(Avg('puntuacion'))['puntuacion__avg']
        return round(resultado, 1) if resultado is not None else 0.0

    # Opcional: Para saber cuántas personas han votado
    @property
    def total_votos(self):
        return self.ratings_recibidos.count()

    
    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"


# Hacemos unas clase (tabla de datos) para almacenar las valoraciones que los usuarios hacen a otros usuarios.
class Rating(models.Model):
    # Cada valoración pertenece a una orden específica
    orden = models.OneToOneField('orden.Order', on_delete=models.CASCADE, related_name='rating')
    # Usuario que hace la valoración
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_dados')
    # Perfil que recibe la valoración
    perfil_destino = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_recibidos')
    
    OPCIONES_VALORACION = [
        (1, '⭐ (1/5) - Muy malo'),
        (2, '⭐⭐ (2/5) - Regular'),
        (3, '⭐⭐⭐ (3/5) - Bueno'),
        (4, '⭐⭐⭐⭐ (4/5) - Muy bueno'),
        (5, '⭐⭐⭐⭐⭐ (5/5) - Excelente'),
    ]
    puntuacion = models.IntegerField(choices=OPCIONES_VALORACION, verbose_name="Puntuación")
    comentario = models.TextField("Comentario", blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Valoración"
        verbose_name_plural = "Valoraciones"

    def __str__(self):
        return f"{self.autor.username} valoró a {self.perfil_destino.user.username} con {self.puntuacion} estrellas"
 """
    


from django.contrib import admin
from .models import UserProfile


# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    


""" @admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('autor', 'perfil_destino', 'puntuacion', 'fecha')
    list_filter = ('autor','puntuacion', 'fecha') """
    
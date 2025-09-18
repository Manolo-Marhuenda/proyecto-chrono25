from django.contrib import admin
from .models import ItemDeOrden

# Register your models here.
@admin.register(ItemDeOrden)
class ItemDeOrdenAdmin(admin.ModelAdmin):
    list_display = ("reloj", "orden")

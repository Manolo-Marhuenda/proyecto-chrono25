from django.contrib import admin
from .models import OrdenDeCompra

# Register your models here.
@admin.register(OrdenDeCompra)
class OrdenDeCompraAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "fecha_orden", "completada", "metodo_pago", "direccion_envio", "get_total_orden")
    list_filter = ("completada", "metodo_pago", "fecha_orden")
    search_fields = ("cliente__username", "direccion_envio")
    ordering = ("-fecha_orden",)
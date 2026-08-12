from django.contrib import admin

# Register your models here.
from django.contrib import admin
from orden.models import Order
from ordenitem.models import OrderItem 

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # Para que no aparezcan filas vacías innecesarias
    readonly_fields = ('price',) # Opcional: para evitar modificar el precio congelado manualmente desde el admin

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'estado') # Campos visibles en la lista
    list_filter = ('estado', 'created_at')
    inlines = [OrderItemInline] # <-- ¡Aquí integramos los OrderItems!
from django.db import models
from django.contrib.auth.models import User
from category.models import Category

# Create your models here.

# Este producto es referido a relojes de segunda mano. 
# ya que nuestra aplicacion es un marketplace de relojes de segunda mano. 
class Product(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relojes')
    marca = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Añadimos catregoria como un campo de clave foránea que se relaciona con el modelo Category. 
    #un reloj solo tiene un acategoria, pero una categoria puede tener muchos relojes.
    category = models.ForeignKey('category.Category',on_delete=models.PROTECT)
    is_sold = models.BooleanField(default=False, verbose_name="Vendido")

    def __str__(self):
        return f"{self.vendedor.username} - {self.marca} - {self.category.nombre} - {self.price}€"

    class Meta:
        verbose_name = "Reloj"
        verbose_name_plural = "Relojes"
        ordering = ['-created_at']

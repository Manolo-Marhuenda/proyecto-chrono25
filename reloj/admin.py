from django.contrib import admin
from .models import Reloj
from profiles.models import UserProfile

# Register your models here.

@admin.register(Reloj)
class RelojAdmin(admin.ModelAdmin):
    list_display = ("user","marca", "modelo","image", "price", "stock")
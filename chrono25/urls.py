"""
URL configuration for chrono25 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import HomeView, LoginView, RegisterView, contacto, LegaltView
from .views import logout_view
from .views import ProfileDetailView, ProfileUpdateView
from reloj.views import RelojCreateView, RelojDetailView
from .views import AgregarAlCarritoView, CarritoView, EliminarDelCarritoView, CrearOrdenCompraView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('contact/', contacto, name='contact'),
    path('profile/<pk>', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update/<pk>', ProfileUpdateView.as_view(), name='profile_update'),
    path('reloj/create/', RelojCreateView.as_view(), name='reloj_create'),
    path('reloj/<pk>/', RelojDetailView.as_view(), name='reloj_detail'),
    path('agregar/<int:reloj_id>/', AgregarAlCarritoView.as_view(), name='agregar_al_carrito'),
    path('carrito/', CarritoView.as_view(), name='ver_carrito_cbv'),
    path('carrito/eliminar/<int:reloj_id>/', EliminarDelCarritoView.as_view(), name='eliminar_del_carrito'),
    path('ordenar/', CrearOrdenCompraView.as_view(), name='orden_creada'),
    path('legal/', LegaltView.as_view(), name='legal'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.forms import forms
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView, UpdateView
from django.views.generic.edit import CreateView, FormView
from .forms import RegistrationForm, LoginForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages

from profiles.models import UserProfile


from django.contrib.auth import authenticate, login, logout




class Homeview(TemplateView):
    template_name = 'general/home.html' 


class loginview(FormView):
    template_name = 'general/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        # Aquí puedes realizar la autenticación del usuario
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f'Inicio de sesión exitoso. Bienvenido: {user.username}')
            return HttpResponseRedirect(reverse_lazy('home'))  # Redirige a la página de inicio después del login exitoso
        else:
            messages.add_message(self.request, messages.ERROR, 'Nombre de usuario o contraseña incorrectos.')
            return self.form_invalid(form)


class registerview(CreateView):
    model = User
    template_name = 'general/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Aquí puedes realizar acciones adicionales después de guardar el usuario
        messages.add_message(self.request, messages.SUCCESS, 'Registro exitoso. Ahora puedes iniciar sesión.')
        return response


class Legalview(TemplateView):
    template_name = 'general/legal.html'


class Contactview(TemplateView):
    template_name = 'general/contacto.html'


class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'general/profile_detail.html'
    context_object_name = 'profile'


class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = 'general/profile_update.html'
    fields = ['photo', 'biography']
    success_url = reverse_lazy('profile_detail')  # Redirige a la página de detalle del perfil después de la actualización

    def form_valid(self, form):
        # Asignar el usuario actual al perfil antes de guardar
        messages.add_message(self.request, messages.SUCCESS, 'Perfil actualizado con éxito.')
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        # Redirige a la página de detalle del perfil después de la actualización
        return reverse_lazy('profile_detail', kwargs={'pk': self.object.pk})



def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Has cerrado sesión correctamente.')
    return HttpResponseRedirect(reverse_lazy('home'))
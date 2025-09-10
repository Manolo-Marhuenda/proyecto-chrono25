from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from profiles.models import UserProfile
from django.views.generic import ListView
from reloj.models import Reloj
from .forms import RegistrationForm, LoginForm
from django.views.generic.edit import FormView
from django.views.generic import DetailView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




class HomeView(ListView):
    template_name = 'general/home.html'
    model = Reloj
    context_object_name = 'relojes' # Nombre para acceder a la lista en la plantilla
    paginate_by = 10 # Número de elementos por página


class LoginView(FormView):
    template_name = 'general/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        usuario = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=usuario, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f'Bienvenido de nuevo {user.username}')
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            messages.add_message(self.request, messages.ERROR, 'Usuario o contraseña incorrectos')
            return super(LoginView, self).form_invalid(form)



class RegisterView(CreateView):
    template_name = 'general/register.html'
    model = User
    success_url = reverse_lazy('login')
    form_class = RegistrationForm

    def form_valid(self, form):
        user = form.save()
        messages.add_message(self.request, messages.SUCCESS, "Usuario creado correctamente.")
        return super(RegisterView,self).form_valid(form)
    


class ContactView(TemplateView):
    template_name = 'general/contact.html'


class LegaltView(TemplateView):
    template_name = 'general/legal.html'


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    template_name = 'general/profile_detail.html'
    model = UserProfile
    context_object_name = 'profile'


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    template_name = 'general/profile_update.html'
    model = UserProfile
    context_object_name = 'profile'
    fields = ['pais', 'profile_picture']

    def form_valid(self, form):
        user = form.save()
        messages.add_message(self.request, messages.SUCCESS, "Perfil actualizado correctamente.")
        return super(ProfileUpdateView,self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'pk': self.object.pk})

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Has cerrado sesión correctamente.')
    return HttpResponseRedirect(reverse_lazy('home'))
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from .models import Reloj
from .forms import RelojForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

@method_decorator(login_required, name='dispatch')
class RelojCreateView(CreateView):
    template_name = 'reloj/reloj_create.html'
    model = Reloj
    form_class= RelojForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Reloj nuevo subido correctamente.")
        return super(RelojCreateView, self).form_valid(form)
    

@method_decorator(login_required, name='dispatch')
class RelojDetailView(DetailView, CreateView):
    template_name = 'reloj/reloj_detail.html'
    model = Reloj
    form_class= RelojForm
    context_object_name = 'reloj'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.reloj = self.get_object()
        return super(RelojDetailView, self).form_valid(form)
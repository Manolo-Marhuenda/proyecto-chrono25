from django.shortcuts import render
from django.views.generic import CreateView
from .models import Reloj
from .forms import RelojForm
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.


class RelojCreateView(CreateView):
    template_name = 'reloj/reloj_create.html'
    model = Reloj
    form_class= RelojForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.add_message(self.request, messages.SUCCESS, "Reloj nuevo subido correctamente.")
        return super(RelojCreateView, self).form_valid(form)
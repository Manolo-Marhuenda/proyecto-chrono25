from django.views.generic import TemplateView


class Homeview(TemplateView):
    template_name = 'general/home.html' 


class loginview(TemplateView):
    template_name = 'general/login.html'


class registerview(TemplateView):
    template_name = 'general/register.html'


class Legalview(TemplateView):
    template_name = 'general/legal.html'


class Contactview(TemplateView):
    template_name = 'general/contacto.html'
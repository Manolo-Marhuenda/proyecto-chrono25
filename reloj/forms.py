from django import forms
from .models import Reloj

class RelojForm(forms.ModelForm):
    class Meta:
        model = Reloj
        fields = ['marca', 'modelo', 'image', 'description', 'price']
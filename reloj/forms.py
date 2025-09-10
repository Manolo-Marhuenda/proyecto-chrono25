from .models import Reloj
from django import forms

class RelojForm(forms.ModelForm):
    class Meta:
        model = Reloj
        fields = ['marca', 'modelo', 'image', 'description', 'price']
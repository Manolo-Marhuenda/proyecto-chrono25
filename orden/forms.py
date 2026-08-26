from django import forms
from .models import Valoracion


class ValoracionForm(forms.ModelForm):
    puntuacion = forms.ChoiceField(
        choices=[(i, f"{i} ★") for i in range(5, 0, -1)],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Puntuación"
    )

    class Meta:
        model = Valoracion
        fields = ['puntuacion', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': '¿Cómo fue tu experiencia con este vendedor y el pedido?'
            }),
        }
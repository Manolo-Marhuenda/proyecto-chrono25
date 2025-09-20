from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from profiles.models import UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
            
            # Utiliza get_or_create para evitar la duplicación del perfil
            UserProfile.objects.get_or_create(user=user)
        
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Password')


class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Tu nombre")
    correo = forms.EmailField(label="Tu correo electrónico")
    mensaje = forms.CharField(widget=forms.Textarea, label="Tu mensaje")







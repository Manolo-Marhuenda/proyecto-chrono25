from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def save(self):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password'])
        user.save()

        from profiles.models import UserProfile
        UserProfile.objects.create(user=user)
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Password')





    




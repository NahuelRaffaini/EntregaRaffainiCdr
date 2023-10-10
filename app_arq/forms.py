from django import forms
from .models import Mensaje
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User



class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['destinatario', 'contenido']

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')
class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
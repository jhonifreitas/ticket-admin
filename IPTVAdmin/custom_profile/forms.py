from django import forms
from django.contrib.auth.forms import AuthenticationForm

from IPTVAdmin.core import utils
from IPTVAdmin.custom_profile import models


class LoginForm(AuthenticationForm):

    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Usuário'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))


class ProfileForm(forms.ModelForm):

    class Meta:
        model = models.Profile
        exclude = ['user', 'points', 'deleted_at']

    first_name = forms.CharField(label='Nome')
    last_name = forms.CharField(label='Sobrenome', required=False)
    username = forms.CharField(label="Usuário")
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())
    password1 = forms.CharField(label='Confirme sua senha', widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if models.User.objects.filter(username=username).exists():
            self.add_error('username', 'Usuário já existe!')
        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if (password and password1) and (password != password1):
            self.add_error('password1', 'Senhas não são iguais!')
        return self.cleaned_data

    def save(self):
        profile = None
        if not self.initial.get('id'):
            data = self.cleaned_data.copy()
            data.pop('password1')
            data_user = {
                'first_name': data.pop('first_name'),
                'last_name': data.pop('last_name'),
                'username': data.pop('username'),
                'password': data.pop('password'),
            }
            user = models.User.objects.create_user(**data_user)
            profile = models.Profile.objects.create(user=user, **data)
        else:
            profile = super().save()
            profile.user.first_name = self.cleaned_data.get('first_name')
            profile.user.last_name = self.cleaned_data.get('last_name')
            profile.user.save()

        if self.initial.get('id') and self.cleaned_data.get('password'):
            self.instance.user.set_password(self.cleaned_data.get('password'))

        return profile

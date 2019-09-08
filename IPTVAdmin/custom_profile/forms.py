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
        exclude = ['config', 'deleted_at']

    cpf = forms.CharField(label='CPF')
    phone = forms.CharField(label='Telefone')

    def clean_cpf(self):
        cpf = utils.CPF(self.cleaned_data.get('cpf'))
        if not cpf.validate():
            raise forms.ValidationError('CPF inválido!')
        return cpf.cleaning()

    def clean_phone(self):
        return utils.Phone(self.cleaned_data.get('phone')).cleaning()

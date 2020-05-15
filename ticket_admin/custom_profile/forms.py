from django import forms
from django.contrib.auth.forms import AuthenticationForm

from ticket_admin.core import utils
from ticket_admin.custom_profile import models


class LoginForm(AuthenticationForm):

    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Usuário'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))


class ProfileForm(forms.ModelForm):

    class Meta:
        model = models.Profile
        exclude = ['user', 'deleted_at']

    cpf = forms.CharField(label='CPF', max_length=14, required=False)
    phone = forms.CharField(label='Telefone')

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            cpf = utils.CPF(cpf)
            if not cpf.validate():
                raise forms.ValidationError('CPF inválido!')
            cpf = cpf.cleaning()
        return cpf

    def clean_phone(self):
        return utils.Phone(self.cleaned_data.get('phone')).cleaning()


class ProfileUserForm(forms.ModelForm):

    class Meta:
        model = models.ProfileUser
        exclude = ['status', 'deleted_at']
        widgets = {
            'expiration': forms.HiddenInput()
        }

    value = forms.CharField(label='Valor', max_length=10)

    def clean_value(self):
        value = self.cleaned_data.get('value')
        return value.replace('.', '').replace(',', '.')

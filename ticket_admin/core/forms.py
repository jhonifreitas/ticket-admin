from django import forms
from django.contrib.auth.password_validation import validate_password

from ticket_admin.core import models


class ConfigForm(forms.ModelForm):

    class Meta:
        model = models.Config
        exclude = ['deleted_at']

    email = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and hasattr(self.instance, 'user'):
            self.fields.get('email').initial = self.instance.user.email


class PasswordResetForm(forms.Form):

    password_old = forms.CharField(label='Senha antiga', widget=forms.PasswordInput())
    password = forms.CharField(label='Nova senha', widget=forms.PasswordInput())
    password1 = forms.CharField(label='Confirme sua nova senha', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_password_old(self):
        value = self.cleaned_data.get('password_old')
        if not self.user.check_password(value):
            raise forms.ValidationError('Senha inválida!')
        return value

    def clean_password(self):
        value = self.cleaned_data.get('password')
        validate_password(value)
        return value

    def clean(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if (password and password1) and (password != password1):
            self.add_error('password1', 'Senhas não são iguais!')

        return self.cleaned_data

    def save(self):
        self.user.set_password(self.cleaned_data.get('password'))
        self.user.save()

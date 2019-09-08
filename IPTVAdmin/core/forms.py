from django import forms

from IPTVAdmin.core import models


class ConfigForm(forms.ModelForm):

    class Meta:
        model = models.Config
        exclude = ['deleted_at']

    email = forms.EmailField(label='Email')
    amount_billet = forms.CharField(label='Valor', max_length=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and hasattr(self.instance, 'user'):
            self.fields.get('email').initial = self.instance.user.email

    def clean_amount_billet(self):
        money = self.cleaned_data.get('amount_billet')
        return money.replace('.', '').replace(',', '.')

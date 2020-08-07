from django import forms

from ticket_admin.bank import models
from ticket_admin.core.utils import CPF


class BankForm(forms.ModelForm):

    class Meta:
        model = models.Bank
        exclude = ['user', 'deleted_at']

    cpf = forms.CharField(label='CPF', max_length=14, required=False)

    def clean_cpf(self):
        value = self.cleaned_data.get('cpf')
        if value:
            cpf = CPF(value)
            if not cpf.validate():
                raise forms.ValidationError('CPF inválido!')
            return cpf.cleaning()
        return value

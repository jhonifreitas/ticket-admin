from django import forms
from datetime import datetime

from ticket_admin.billet import models


class BilletForm(forms.ModelForm):

    class Meta:
        model = models.Billet
        exclude = ['code', 'paymentLink', 'barcode', 'reference', 'status', 'deleted_at']
        widgets = {
            'dueDate': forms.HiddenInput(),
            'instructions': forms.TextInput(attrs={'readonly': True})
        }

    amount = forms.CharField(label='Valor', max_length=10)

    def clean_amount(self):
        money = self.cleaned_data.get('amount')
        return money.replace('.', '').replace(',', '.')


class BilletImportForm(forms.Form):

    initial_date = forms.DateField(label='Data inicial', widget=forms.DateInput(attrs={'autocomplete': 'off'}))
    final_date = forms.DateField(label='Data final', widget=forms.DateInput(attrs={'autocomplete': 'off'}))

    def clean_initial_date(self):
        value = self.cleaned_data.get('initial_date')
        if value >= datetime.now().date():
            raise forms.ValidationError('A data deve ser menor do que a data atual!')
        return value

    def clean_final_date(self):
        value = self.cleaned_data.get('final_date')
        if value > datetime.now().date():
            raise forms.ValidationError('A data deve ser menor do que a data atual!')
        return value

    def clean(self):
        initial_date = self.cleaned_data.get('initial_date')
        final_date = self.cleaned_data.get('final_date')

        if initial_date and final_date:
            if initial_date >= final_date:
                raise forms.ValidationError('A data inicial deve ser menor que a data final!')
            between_date = final_date - initial_date
            if between_date.days > 30:
                raise forms.ValidationError('O intervalo das datas devem ser menor ou igual a 30 dias!')
        return super().clean()

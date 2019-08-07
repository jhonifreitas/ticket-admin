from django import forms

from IPTVAdmin.billet import models


class BilletForm(forms.ModelForm):

    class Meta:
        model = models.Billet
        exclude = ['code', 'paymentLink', 'barcode', 'dueDate', 'reference', 'status', 'deleted_at']

    amount = forms.CharField(label='Valor')

    def clean_amount(self):
        money = self.cleaned_data.get('amount')
        return money.replace('.', '').replace(',', '.')
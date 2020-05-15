from django import forms

from ticket_admin.billet import models


class BilletForm(forms.ModelForm):

    class Meta:
        model = models.Billet
        exclude = ['code', 'paymentLink', 'barcode', 'reference', 'status', 'deleted_at']
        widgets = {
            'dueDate': forms.HiddenInput(),
            'instructions': forms.TextInput(attrs={'readonly': True})
        }

    tax_message = 'Será descontado o valor de R$ 2,90 após o pagamento do boleto!<br>'\
                  'Será cobrado o valor adicional de 1 real pelo boleto!<br>'\
                  'Obs: taxas do pagseguro'

    amount = forms.CharField(
        label='Valor', max_length=10,
        help_text=tax_message)

    def clean_amount(self):
        money = self.cleaned_data.get('amount')
        return money.replace('.', '').replace(',', '.')

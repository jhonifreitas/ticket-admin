from django import forms

from ticket_admin.payment import models


class PaymentForm(forms.ModelForm):

    class Meta:
        model = models.Payment
        exclude = ['user', 'status', 'deleted_at']
        widgets = {
            'date': forms.HiddenInput()
        }

    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'd-none'}), required=False)

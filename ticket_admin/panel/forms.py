from django import forms

from ticket_admin.panel import models


class PanelForm(forms.ModelForm):

    class Meta:
        model = models.Panel
        exclude = ['user', 'deleted_at']

    value = forms.CharField(label='Valor do crédito', max_length=10)

    def clean_value(self):
        value = self.cleaned_data.get('value')
        return value.replace('.', '').replace(',', '.')

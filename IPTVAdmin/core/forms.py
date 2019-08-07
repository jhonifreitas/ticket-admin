from django import forms

from IPTVAdmin.core import models


class ConfigForm(forms.ModelForm):

    class Meta:
        model = models.Config
        exclude = ['deleted_at']
    
    email = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields.get('email').initial = self.instance.user.email

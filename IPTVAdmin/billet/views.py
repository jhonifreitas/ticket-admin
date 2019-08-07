import json
import requests
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render

from IPTVAdmin.core import views
from IPTVAdmin.billet import models, forms
from IPTVAdmin.custom_profile.models import Profile


class BilletListView(views.BaseListView):

    paginate_by = 10
    model = models.Billet
    template_name = 'billet/list.html'
    permission_required = ['billet.list_billet']

    def get_queryset(self):
        object_list = super().get_queryset()
        # text_filter = self.request.GET.get('q')
        # if hasattr(self.request.user, 'dealer'):
        #     object_list = object_list.filter(dealer=self.request.user.dealer)
        # if text_filter:
        #     object_list = object_list.filter(
        #         Q(user__username__icontains=text_filter) |
        #         Q(user__first_name__icontains=text_filter) |
        #         Q(user__last_name__icontains=text_filter))
        return object_list


class BilletCreateView(views.BaseCreateView):

    model = models.Billet
    form_class = forms.BilletForm
    template_name = 'billet/form.html'
    success_url = reverse_lazy('billet:list')
    success_message = 'Boleto cadastrado!'
    permission_required = ['billet.add_billet']

    def get_initial(self):
        initial = self.initial.copy()
        initial['instructions'] = self.request.user.config.instructions_billet
        initial['description'] = self.request.user.config.description_billet
        initial['amount'] = self.request.user.config.amount_billet
        profile_uuid = self.request.GET.get('profile')
        if profile_uuid:
            initial['profile'] = get_object_or_404(Profile, uuid=profile_uuid)
        return initial
    
    def form_valid(self, form):
        form.instance.reference = form.cleaned_data.get('profile').name
        url = f'{settings.PAGSEGURO_BOLETO_URL}?email={self.request.user.email}&token={self.request.user.config.token}'
        data = {
            "reference": form.cleaned_data.get('profile').name,
            "firstDueDate": str(form.cleaned_data.get('firstDueDate')),
            "numberOfPayments": form.cleaned_data.get('numberOfPayments'),
            "periodicity": "monthly",
            "amount": form.cleaned_data.get('amount'),
            "instructions": form.cleaned_data.get('instructions'),
            "description": form.cleaned_data.get('description'),
            "customer": {
                "document": {
                    "type": "CPF",
                    "value": "00000000000"
                },
                "name": form.cleaned_data.get('profile').name,
                "email": form.cleaned_data.get('profile').email,
                "phone": {
                    "areaCode": form.cleaned_data.get('profile').phone[:2],
                    "number": form.cleaned_data.get('profile').phone[2:]
                }
            }
        }
        response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        if response.ok:
            from IPython import embed; embed()
            return super().form_valid(form)
        for err in response.json().get('errors'):
            messages.error(self.request, err.get('message'))
            return render(self.request, self.template_name, self.get_context_data(form=self.get_form()))
        return self.form_invalid(form)

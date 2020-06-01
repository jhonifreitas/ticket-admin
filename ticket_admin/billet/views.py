from datetime import datetime, timedelta

from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from ticket_admin.core import views
from ticket_admin.billet import models, forms
from ticket_admin.billet.pagseguro import Pagseguro
from ticket_admin.custom_profile.models import Profile


class BilletListView(views.BaseListView):

    model = models.Billet
    template_name = 'billet/list.html'
    permission_required = ['billet.list_billet']

    def get_queryset(self):
        object_list = super().get_queryset().filter(profile__user__config=self.request.user.config)
        text_filter = self.request.GET.get('q')
        status_filter = self.request.GET.get('status')
        if text_filter:
            object_list = object_list.filter(
                Q(profile__name__icontains=text_filter) |
                Q(profile__email__icontains=text_filter) |
                Q(profile__phone__icontains=text_filter))
        if status_filter:
            object_list = object_list.filter(status=status_filter)
        return object_list


class BilletCreateView(views.BaseCreateView):

    model = models.Billet
    pagseguro = Pagseguro()
    form_class = forms.BilletForm
    template_name = 'billet/form.html'
    success_url = reverse_lazy('billet:list')
    success_message = 'Boleto cadastrado!'
    permission_required = ['billet.add_billet']

    def get_initial(self):
        initial = self.initial.copy()
        tomorrow = datetime.now().date() + timedelta(days=1)
        dueDate = self.request.GET.get('dueDate', tomorrow)

        if isinstance(dueDate, str) and datetime.strptime(dueDate, '%Y-%m-%d').date() < tomorrow:
            dueDate = tomorrow

        initial['dueDate'] = dueDate
        initial['amount'] = self.request.GET.get('amount', None)
        initial['description'] = self.request.user.config.description_billet
        initial['instructions'] = self.request.user.config.instructions_billet

        profile_uuid = self.request.GET.get('profile')
        if profile_uuid:
            initial['profile'] = get_object_or_404(Profile, uuid=profile_uuid)
        return initial

    def form_valid(self, form):
        form.instance.reference = form.cleaned_data.get('profile').name

        self.pagseguro.set_config(self.request.user.config)
        response = self.pagseguro.generate_ticket(form.cleaned_data)
        result_json = response.json()

        if response.ok:
            for billet in result_json.get('boletos'):
                form.instance.code = billet.get('code')
                form.instance.barcode = billet.get('barcode')
                form.instance.paymentLink = billet.get('paymentLink').replace('print.jhtml', 'print_image.jhtml')
                form.save()
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)

        if result_json.get('errors'):
            for err in result_json.get('errors'):
                messages.error(self.request, err.get('message'))
        elif result_json.get('error'):
            messages.error(self.request, result_json.get('message'))

        return self.form_invalid(form)


class BilletSyncView(views.BaseView):

    model = models.Billet
    pagseguro = Pagseguro()
    success_url = reverse_lazy('billet:list')
    success_message = 'Boleto sincronizado!'
    permission_required = ['billet.list_billet']

    def get(self, request, code):
        obj = get_object_or_404(self.model, code=code)
        self.pagseguro.set_config(self.request.user.config)
        ticket = self.pagseguro.get_transaction(code)
        if ticket:
            obj.status = ticket.get('status')
            obj.amount = ticket.get('amount')
            obj.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        messages.error(request, 'Boleto não encontrado!')
        return redirect(self.success_url)

from django.urls import reverse_lazy

from ticket_admin.core import views
from ticket_admin.bank import models, forms


class BankListView(views.BaseListView):

    model = models.Bank
    template_name = 'bank/list.html'
    permission_required = ['bank.list_bank']

    def get_queryset(self):
        object_list = super().get_queryset().filter(user=self.request.user)
        text_filter = self.request.GET.get('q')
        if text_filter:
            object_list = object_list.filter(name__icontains=text_filter)
        return object_list


class BankCreateView(views.BaseCreateView):

    model = models.Bank
    form_class = forms.BankForm
    template_name = 'bank/form.html'
    success_url = reverse_lazy('bank:list')
    success_message = 'Banco cadastrado!'
    permission_required = ['bank.add_bank']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BankUpdateView(views.BaseUpdateView):

    model = models.Bank
    form_class = forms.BankForm
    template_name = 'bank/form.html'
    success_url = reverse_lazy('panel:list')
    success_message = 'Banco salvo!'
    permission_required = ['bank.change_bank']


class BankDeleteView(views.BaseDeleteView):

    model = models.Bank
    template_name = 'bank/list.html'
    success_url = reverse_lazy('bank:list')
    success_message = 'Banco deletado!'
    permission_required = ['bank.delete_bank']

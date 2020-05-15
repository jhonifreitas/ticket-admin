from datetime import datetime

from django.urls import reverse_lazy

from ticket_admin.core import views
from ticket_admin.payment import models, forms


class PaymentListView(views.BaseListView):

    model = models.Payment
    template_name = 'payment/list.html'
    permission_required = ['payment.list_payment']

    def get_queryset(self):
        object_list = super().get_queryset().filter(user=self.request.user)
        text_filter = self.request.GET.get('q')
        if text_filter:
            object_list = object_list.filter(name__icontains=text_filter)
        return object_list


class PaymentCreateView(views.BaseCreateView):

    model = models.Payment
    form_class = forms.PaymentForm
    template_name = 'payment/form.html'
    success_url = reverse_lazy('payment:list')
    success_message = 'Pagamento cadastrado!'
    permission_required = ['payment.add_payment']
    initial = {
        'date': datetime.now().date()
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PaymentDetailView(views.BaseDetailView):

    model = models.Payment
    template_name = 'payment/detail.html'
    permission_required = ['payment.view_payment']


class PaymentDeleteView(views.BaseDeleteView):

    model = models.Payment
    template_name = 'payment/list.html'
    success_url = reverse_lazy('payment:list')
    success_message = 'Painel deletado!'
    permission_required = ['payment.delete_payment']

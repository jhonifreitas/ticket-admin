from django.urls import reverse_lazy

from ticket_admin.core import views
from ticket_admin.panel import models, forms


class PanelListView(views.BaseListView):

    model = models.Panel
    template_name = 'panel/list.html'
    permission_required = ['panel.list_panel']

    def get_queryset(self):
        object_list = super().get_queryset().filter(user=self.request.user)
        text_filter = self.request.GET.get('q')
        if text_filter:
            object_list = object_list.filter(name__icontains=text_filter)
        return object_list


class PanelCreateView(views.BaseCreateView):

    model = models.Panel
    form_class = forms.PanelForm
    template_name = 'panel/form.html'
    success_url = reverse_lazy('panel:list')
    success_message = 'Painel cadastrado!'
    permission_required = ['panel.add_panel']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PanelUpdateView(views.BaseUpdateView):

    model = models.Panel
    form_class = forms.PanelForm
    template_name = 'panel/form.html'
    success_url = reverse_lazy('panel:list')
    success_message = 'Painel salvo!'
    permission_required = ['panel.change_panel']


class PanelDeleteView(views.BaseDeleteView):

    model = models.Panel
    template_name = 'panel/list.html'
    success_url = reverse_lazy('panel:list')
    success_message = 'Painel deletado!'
    permission_required = ['panel.delete_panel']

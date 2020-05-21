from django.db.models import Q
from django.db import transaction
from django.urls import reverse_lazy

from ticket_admin.core import views
from ticket_admin.custom_profile import models, forms


class ProfileListView(views.BaseListView):

    model = models.Profile
    template_name = 'profile/list.html'
    permission_required = ['custom_profile.list_profile']

    def get_queryset(self):
        object_list = super().get_queryset().filter(user=self.request.user)
        text_filter = self.request.GET.get('q')
        if text_filter:
            object_list = object_list.filter(
                Q(name__icontains=text_filter) |
                Q(phone__icontains=text_filter))
        return object_list


class ProfileCreateView(views.BaseCreateView):

    model = models.Profile
    form_class = forms.ProfileForm
    template_name = 'profile/form.html'
    success_url = reverse_lazy('profile:list')
    success_message = 'Usuário cadastrado!'
    permission_required = ['custom_profile.add_profile']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = forms.ProfileUserFormSet(form_kwargs={'user': self.request.user})
        if self.request.POST:
            context['users'] = forms.ProfileUserFormSet(self.request.POST, form_kwargs={'user': self.request.user})
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        users = context.get('users')
        with transaction.atomic():
            self.object = form.save()
            if users.is_valid():
                users.instance = self.object
                users.save()
        return super().form_valid(form)


class ProfileUpdateView(views.BaseUpdateView):

    model = models.Profile
    form_class = forms.ProfileForm
    template_name = 'profile/form.html'
    success_url = reverse_lazy('profile:list')
    success_message = 'Usuário salvo!'
    permission_required = ['custom_profile.change_profile']


class ProfileDeleteView(views.BaseDeleteView):

    model = models.Profile
    template_name = 'profile/list.html'
    success_url = reverse_lazy('profile:list')
    success_message = 'Usuário deletado!'
    permission_required = ['custom_profile.delete_profile']

from datetime import datetime
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from ticket_admin.core import views
from ticket_admin.custom_profile import models, forms


class ProfileUserListView(views.BaseListView):

    model = models.ProfileUser
    template_name = 'profile/users/list.html'
    permission_required = ['custom_profile.list_profileuser']

    def get_profile_uuid(self):
        return self.request.GET.get('profile')

    def get_queryset(self):
        object_list = super().get_queryset()
        if self.get_profile_uuid():
            object_list = object_list.filter(profile__uuid=self.get_profile_uuid())

        text_filter = self.request.GET.get('q')
        if text_filter:
            object_list = object_list.filter(
                Q(username__icontains=text_filter) |
                Q(password__icontains=text_filter) |
                Q(profile__name__icontains=text_filter) |
                Q(panel__name__icontains=text_filter) |
                Q(observation__icontains=text_filter) |
                Q(status__icontains=text_filter))
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.get_profile_uuid():
            context['profile'] = get_object_or_404(models.Profile, uuid=self.get_profile_uuid())
        return context


class ProfileUserCreateView(views.BaseCreateView):

    model = models.ProfileUser
    form_class = forms.ProfileUserForm
    success_message = 'Usuário cadastrado!'
    template_name = 'profile/users/form.html'
    success_url = reverse_lazy('profile:user-list')
    permission_required = ['custom_profile.add_profileuser']
    initial = {
        'expiration': datetime.now().date()
    }

    def get_profile_uuid(self):
        return self.request.GET.get('profile')

    def get_profile(self):
        return get_object_or_404(models.Profile, uuid=self.get_profile_uuid())

    def get_initial(self):
        initial = super().get_initial()
        if self.get_profile_uuid():
            initial['profile'] = self.get_profile().id
        return initial

    def form_valid(self, form):
        if self.get_profile_uuid():
            form.instance.profile = self.get_profile()
        return super().form_valid(form)

    def get_success_url(self):
        url = super().get_success_url()
        if self.get_profile_uuid():
            url += '?profile={}'.format(self.get_profile_uuid())
        return url


class ProfileUserUpdateView(views.BaseUpdateView):

    model = models.ProfileUser
    form_class = forms.ProfileUserForm
    success_message = 'Usuário salvo!'
    template_name = 'profile/users/form.html'
    success_url = reverse_lazy('profile:user-list')
    permission_required = ['custom_profile.change_profileuser']

    def get_success_url(self):
        url = super().get_success_url()
        profile_uuid = self.request.GET.get('profile')
        if profile_uuid:
            url += '?profile={}'.format(profile_uuid)
        return url


class ProfileUserDeleteView(views.BaseDeleteView):

    model = models.ProfileUser
    success_message = 'Usuário deletado!'
    template_name = 'profile/users/list.html'
    success_url = reverse_lazy('profile:user-list')
    permission_required = ['custom_profile.delete_profileuser']

    def get_success_url(self):
        url = super().get_success_url()
        profile_uuid = self.request.GET.get('profile')
        if profile_uuid:
            url += '&profile={}'.format(profile_uuid)
        return url

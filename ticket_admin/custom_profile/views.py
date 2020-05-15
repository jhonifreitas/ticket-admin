from datetime import datetime
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

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

    def form_valid(self, form):
        form.instance.user = self.request.user
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


# ================================================================================================
# PROFILE - USER
# ================================================================================================


class ProfileUserListView(views.BaseListView):

    model = models.ProfileUser
    template_name = 'profile/users/list.html'
    permission_required = ['custom_profile.list_profileuser']

    def get_queryset(self):
        object_list = super().get_queryset().filter(profile__uuid=self.kwargs.get('profile_uuid'))
        text_filter = self.request.GET.get('q')
        if text_filter:
            object_list = object_list.filter(
                Q(username__icontains=text_filter) |
                Q(password__icontains=text_filter) |
                Q(panel__name__icontains=text_filter) |
                Q(status__icontains=text_filter))
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['profile'] = get_object_or_404(models.Profile, uuid=self.kwargs.get('profile_uuid'))
        return context


class ProfileUserCreateView(views.BaseCreateView):

    model = models.ProfileUser
    form_class = forms.ProfileUserForm
    template_name = 'profile/users/form.html'
    success_message = 'Usuário cadastrado!'
    permission_required = ['custom_profile.add_profileuser']
    initial = {
        'expiration': datetime.now().date()
    }

    def form_valid(self, form):
        form.instance.profile = get_object_or_404(models.Profile, uuid=self.kwargs.get('profile_uuid'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile:user-list', args=[self.kwargs.get('profile_uuid')])


class ProfileUserUpdateView(views.BaseUpdateView):

    model = models.ProfileUser
    form_class = forms.ProfileUserForm
    template_name = 'profile/users/form.html'
    success_message = 'Usuário salvo!'
    permission_required = ['custom_profile.change_profileuser']

    def get_success_url(self):
        return reverse_lazy('profile:user-list', args=[self.kwargs.get('profile_uuid')])


class ProfileUserDeleteView(views.BaseDeleteView):

    model = models.ProfileUser
    template_name = 'profile/users/list.html'
    success_message = 'Usuário deletado!'
    permission_required = ['custom_profile.delete_profileuser']

    def get_success_url(self):
        return reverse_lazy('profile:user-list', args=[self.kwargs.get('profile_uuid')])

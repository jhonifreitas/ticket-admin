from django.db.models import Q
from django.urls import reverse_lazy

from IPTVAdmin.core import views
from IPTVAdmin.custom_profile import models, forms


class ProfileListView(views.BaseListView):

    paginate_by = 10
    model = models.Profile
    template_name = 'profile/list.html'
    permission_required = ['custom_profile.list_profile']

    def get_queryset(self):
        object_list = super().get_queryset().filter(config=self.request.user.config)
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
        form.instance.config = self.request.user.config
        return super().form_valid(form)


class ProfileUpdateView(views.BaseUpdateView):

    model = models.Profile
    form_class = forms.ProfileForm
    template_name = 'profile/form.html'
    success_url = reverse_lazy('profile:list')
    success_message = 'Usuário salvo!'
    permission_required = ['custom_profile.update_profile']

    # def get_form(self):
    #     form = super().get_form()
    #     form.fields['password'].required = False
    #     form.fields['password1'].required = False
    #     form.fields['first_name'].initial = form.instance.user.first_name
    #     form.fields['last_name'].initial = form.instance.user.last_name
    #     form.fields['username'].initial = form.instance.user.username
    #     return form


class ProfileDeleteView(views.BaseDeleteView):

    model = models.Profile
    template_name = 'profile/list.html'
    success_url = reverse_lazy('profile:list')
    success_message = 'Usuário deletado!'
    permission_required = ['custom_profile.delete_profile']

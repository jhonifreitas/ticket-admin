from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from ticket_admin.core import models, forms
from ticket_admin.billet.models import Billet
from ticket_admin.custom_profile.models import Profile, ProfileUser


class BaseView(PermissionRequiredMixin, SuccessMessageMixin, View):

    raise_exception = True
    permission_required = []

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('billet.list_billet'):
            url_allowed = [
                reverse_lazy('core:config'),
            ]
            if not request.get_full_path() in url_allowed and not hasattr(request.user, 'config'):
                messages.warning(request, 'Configure sua conta antes de continuar!')
                return redirect(reverse_lazy('core:config'))
        return super().dispatch(request, *args, **kwargs)


class BaseListView(BaseView, ListView):

    paginate_by = 10


class BaseCreateView(BaseView, CreateView):

    pass


class BaseUpdateView(BaseView, UpdateView):

    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class BaseDeleteView(BaseView, DeleteView):

    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(BaseDeleteView, self).delete(request, *args, **kwargs)


class BaseDetailView(BaseView, DetailView):

    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class HomeView(BaseView):

    template_name = 'core/home.html'

    def get_context_data(self):
        user = self.request.user
        query_user = ProfileUser.objects.filter(profile__user=user)
        context = {
            'clients': Profile.objects.filter(user=user).count(),
            'users': ProfileUser.objects.filter(profile__user=user).count(),
            'users_active': query_user.filter(status=ProfileUser.ACTIVE).count(),
            'users_waiting': query_user.filter(status=ProfileUser.WAITING).count(),
            'users_expired': query_user.filter(status=ProfileUser.EXPIRED).count(),
            'billing': ProfileUser.objects.get_billing(user),
            'billing_liquid': ProfileUser.objects.get_billing_liquid(user)
        }
        if user.has_perm('billet.list_billet'):
            context['billets_wainting'] = Billet.objects.filter(
                profile__user=user, status=Billet.WAITING).count()
            context['billets_debited'] = Billet.objects.filter(
                Q(status=Billet.PAID) | Q(status=Billet.DEBITED),
                profile__user=user).count()
            context['billets_canceled'] = Billet.objects.filter(
                profile__user=user, status=Billet.CANCELED).count()
            context['billing_billet'] = Billet.objects.get_billing(user)
        return context

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())


class ConfigView(BaseView):

    model = models.Config
    form_class = forms.ConfigForm
    template_name = 'core/config.html'
    success_message = 'Configuração salva!'
    success_url = reverse_lazy('core:config')

    def get_object(self):
        return self.model.objects.filter(user=self.request.user).first()

    def get_context_data(self):
        context = {'form': self.form_class(instance=self.get_object())}
        return context

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request):
        context = self.get_context_data()
        data = request.POST.copy()
        data['user'] = request.user.pk
        form = self.form_class(instance=self.get_object(), data=data)

        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data.get('email')
            request.user.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        context['form'] = form
        return render(request, self.template_name, context=context)


class TutorialView(BaseListView):

    model = models.Tutorial
    template_name = 'core/tutorial/list.html'
    permission_required = ['core.list_tutorial']


class TutorialDetailView(BaseDetailView):

    model = models.Tutorial
    template_name = 'core/tutorial/detail.html'
    permission_required = ['core.view_tutorial']

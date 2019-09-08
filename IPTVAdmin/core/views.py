from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from IPTVAdmin.core import models, forms
from IPTVAdmin.billet.models import Billet
from IPTVAdmin.custom_profile.models import Profile


class BaseView(PermissionRequiredMixin, SuccessMessageMixin, View):

    raise_exception = True
    permission_required = []

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        url_allowed = [
            reverse_lazy('core:config'),
        ]
        if not request.get_full_path() in url_allowed and not hasattr(request.user, 'config'):
            messages.warning(request, 'Configure sua conta antes de continuar!')
            return redirect(reverse_lazy('core:config'))
        return super().dispatch(request, *args, **kwargs)


class BaseListView(BaseView, ListView):

    pass


class BaseCreateView(BaseView, CreateView):

    pass


class BaseUpdateView(BaseView, UpdateView):

    pass


class BaseDeleteView(BaseView, DeleteView):

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(BaseDeleteView, self).delete(request, *args, **kwargs)


class BaseDetailView(BaseView, DetailView):

    def get_object(self):
        return get_object_or_404(self.model.objects.all(), pk=self.kwargs.get('pk'))


class HomeView(BaseView):

    template_name = 'core/home.html'

    def get_context_data(self):
        context = {
            'profiles': Profile.objects_all.count(),
            'billets_pending': Billet.objects.filter(status=Billet.PENDING).count(),
            'billets_approveds': Billet.objects.filter(status=Billet.APPROVED).count(),
            'billets_recuseds': Billet.objects.filter(status=Billet.RECUSED).count()
        }
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
        return self.model.objects.first()

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

from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from IPTVAdmin.custom_profile.models import Profile


class BaseView(PermissionRequiredMixin, SuccessMessageMixin, View):

    raise_exception = True
    permission_required = []

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
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
        }
        return context

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())

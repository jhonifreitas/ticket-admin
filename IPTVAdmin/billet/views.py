from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render

from IPTVAdmin.core import views
from IPTVAdmin.billet import models, forms
from IPTVAdmin.billet.pagseguro import Pagseguro
from IPTVAdmin.custom_profile.models import Profile


class BilletListView(views.BaseListView):

    paginate_by = 10
    model = models.Billet
    template_name = 'billet/list.html'
    permission_required = ['billet.list_billet']

    def get_context_data(self):
        context = super().get_context_data()
        context['form_import'] = forms.BilletImportForm
        return context

    def get_queryset(self):
        object_list = super().get_queryset()
        text_filter = self.request.GET.get('q')
        if text_filter:
            object_list = object_list.filter(
                Q(user__username__icontains=text_filter) |
                Q(user__first_name__icontains=text_filter) |
                Q(user__last_name__icontains=text_filter))
        return object_list


class BilletImportView(views.BaseView):

    model = models.Billet
    form_class = forms.BilletImportForm
    template_name = 'billet/list.html'
    success_url = reverse_lazy('billet:list')
    success_message = 'boletos importados!'
    permission_required = ['billet.list_billet']

    def get_context_data(self):
        return {'object_list': self.model.objects.all()}

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            initialDate = str(form.cleaned_data.get('initial_date'))
            finalDate = str(form.cleaned_data.get('final_date'))

            result = Pagseguro(self.request.user.config).get_transactions(initialDate, finalDate)
            billets = result.get('ok')

            if billets:
                for billet in billets:
                    obj = self.model.objects.filter(code=billet.get('code'))
                    if obj.exists():
                        obj.update(**billet)
                    else:
                        self.model.objects.create(**billet)
                messages.success(request, f'{len(billets)} {self.success_message}')
                return redirect(self.success_url)
            elif result.get('warning'):
                messages.warning(request, result.get('warning'))
            else:
                messages.error(request, result.get('error'))
        context = self.get_context_data()
        context['form_import'] = form
        return render(request, self.template_name, context)


class BilletCreateView(views.BaseCreateView):

    model = models.Billet
    form_class = forms.BilletForm
    template_name = 'billet/form.html'
    success_url = reverse_lazy('billet:list')
    success_message = 'Boleto cadastrado!'
    permission_required = ['billet.add_billet']

    def get_initial(self):
        initial = self.initial.copy()
        initial['instructions'] = self.request.user.config.instructions_billet
        initial['description'] = self.request.user.config.description_billet
        initial['amount'] = self.request.user.config.amount_billet
        profile_uuid = self.request.GET.get('profile')
        if profile_uuid:
            initial['profile'] = get_object_or_404(Profile, uuid=profile_uuid)
        return initial

    def form_valid(self, form):
        form.instance.reference = form.cleaned_data.get('profile').name

        response = Pagseguro(self.request.user.config).generate_ticket(form.cleaned_data)
        result_json = response.json()

        if response.ok:
            for billet in result_json.get('boletos'):
                billet.update(**form.data.dict())
                form = self.form_class(data=billet)
                if form.is_valid():
                    form.save()
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)

        if result_json.get('errors'):
            for err in result_json.get('errors'):
                messages.error(self.request, err.get('message'))
        elif result_json.get('error'):
            messages.error(self.request, result_json.get('message'))

        return self.form_invalid(form)

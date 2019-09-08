from django.urls import path

from IPTVAdmin.billet import views

app_name = 'billet'

urlpatterns = [
    path('', views.BilletListView.as_view(), name='list'),
    path('formulario/', views.BilletCreateView.as_view(), name='create'),

    path('importar/', views.BilletImportView.as_view(), name='import'),
]

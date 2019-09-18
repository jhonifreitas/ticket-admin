from django.urls import path

from ticket_admin.billet import views

app_name = 'billet'

urlpatterns = [
    path('', views.BilletListView.as_view(), name='list'),
    path('formulario/', views.BilletCreateView.as_view(), name='create'),

    path('importar/', views.BilletImportView.as_view(), name='import'),
    path('sincronizar/<str:code>/', views.BilletSyncView.as_view(), name='sync'),
]

from django.urls import path

from ticket_admin.bank import views

app_name = 'bank'

urlpatterns = [
    path('', views.BankListView.as_view(), name='list'),
    path('formulario/', views.BankCreateView.as_view(), name='create'),
    path('formulario/<uuid:uuid>/', views.BankUpdateView.as_view(), name='update'),
    path('<uuid:uuid>/', views.BankDeleteView.as_view(), name='delete'),
]

from django.urls import path

from ticket_admin.payment import views

app_name = 'payment'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='list'),
    path('formulario/', views.PaymentCreateView.as_view(), name='create'),
    path('detalhe/<uuid:uuid>/', views.PaymentDetailView.as_view(), name='detail'),
    path('<uuid:uuid>/', views.PaymentDeleteView.as_view(), name='delete'),
]

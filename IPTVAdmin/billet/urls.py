from django.urls import path
from django.contrib.auth import views as auth_views

from IPTVAdmin.billet import views

app_name = 'billet'

urlpatterns = [
    path('', views.BilletListView.as_view(), name='list'),
    path('formulario/', views.BilletCreateView.as_view(), name='create'),
    # path('formulario/<int:pk>/', views.BilletUpdateView.as_view(), name='update'),
    # path('<int:pk>/', views.BilletDeleteView.as_view(), name='delete'),
]

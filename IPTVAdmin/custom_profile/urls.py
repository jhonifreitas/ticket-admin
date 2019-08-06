from django.urls import path
from django.contrib.auth import views as auth_views

from IPTVAdmin.custom_profile import views, forms

app_name = 'profile'

urlpatterns = [
    path('entrar/', auth_views.LoginView.as_view(authentication_form=forms.LoginForm), name='login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.ProfileListView.as_view(), name='list'),
    path('formulario/', views.ProfileCreateView.as_view(), name='create'),
    path('formulario/<int:pk>/', views.ProfileUpdateView.as_view(), name='update'),
    path('<int:pk>/', views.ProfileDeleteView.as_view(), name='delete'),
]

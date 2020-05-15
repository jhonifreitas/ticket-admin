from django.urls import path
from django.contrib.auth import views as auth_views

from ticket_admin.custom_profile import views, forms

app_name = 'profile'

urlpatterns = [
    path('entrar/', auth_views.LoginView.as_view(authentication_form=forms.LoginForm), name='login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.ProfileListView.as_view(), name='list'),
    path('formulario/', views.ProfileCreateView.as_view(), name='create'),
    path('formulario/<uuid:uuid>/', views.ProfileUpdateView.as_view(), name='update'),
    path('<uuid:uuid>/', views.ProfileDeleteView.as_view(), name='delete'),

    path('usuario/', views.ProfileUserListView.as_view(), name='user-list'),
    path('usuario/formulario/', views.ProfileUserCreateView.as_view(), name='user-create'),
    path('usuario/formulario/<uuid:uuid>/', views.ProfileUserUpdateView.as_view(),
         name='user-update'),
    path('usuario/<uuid:uuid>/', views.ProfileUserDeleteView.as_view(), name='user-delete'),
]

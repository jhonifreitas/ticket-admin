from django.urls import path

from IPTVAdmin.core import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]

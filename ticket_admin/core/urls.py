from django.urls import path

from ticket_admin.core import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('configuracao/', views.ConfigView.as_view(), name='config'),

    # TUTORIAL
    path('tutorial/', views.TutorialView.as_view(), name='list-tutorial'),
    path('tutorial/<uuid:uuid>', views.TutorialDetailView.as_view(), name='detail-tutorial'),
]

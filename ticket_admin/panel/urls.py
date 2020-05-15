from django.urls import path

from ticket_admin.panel import views

app_name = 'panel'

urlpatterns = [
    path('', views.PanelListView.as_view(), name='list'),
    path('formulario/', views.PanelCreateView.as_view(), name='create'),
    path('formulario/<uuid:uuid>/', views.PanelUpdateView.as_view(), name='update'),
    path('<uuid:uuid>/', views.PanelDeleteView.as_view(), name='delete'),
]

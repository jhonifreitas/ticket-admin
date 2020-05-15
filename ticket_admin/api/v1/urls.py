from django.urls import path
from django.urls import include

from rest_framework import routers

from ticket_admin.api.v1.payment import views as payment_views

app_name = 'api.v1'

router = routers.SimpleRouter()

urlpatterns = [
    # PAGSEGURO
    path('billet/notification/', payment_views.PaymentViewSet.as_view({'post': 'post'}), name='notification'),

    path('', include(router.urls)),
]

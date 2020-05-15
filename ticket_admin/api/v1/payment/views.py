from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from ticket_admin.billet.models import Billet
from ticket_admin.billet.pagseguro import Pagseguro


class PaymentViewSet(viewsets.ViewSet):

    pagseguro = Pagseguro()
    model = Billet

    def get_object(self, code):
        return get_object_or_404(self.model, code=code)

    def post(self, request):
        code = request.data.get('notificationCode')
        response = self.pagseguro.get_notification(code)
        if response.ok:
            result = response.json()
            obj = self.get_object(result.get('code'))
            obj.status = result.status
            obj.save()

            return Response({'ok': 'Atualizado!'}, status=status.HTTP_200_OK)
        return Response({'error': response.text}, status=status.HTTP_400_BAD_REQUEST)

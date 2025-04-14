from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.orders.services import PaymentService
from apps.orders.api.serializers import PaymentSerializer

from apps.core.utils.permissions import UserPermission


class PaymentView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = PaymentSerializer

    permission_app_label  = 'orders'
    permission_model = 'order'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = PaymentService()
    
    def get(self, request):
        payment_methods = self.__service.get_all_payment_methods()
        response = self.serializer_class(payment_methods, many=True)

        return Response({'payment_methods': response.data}, status=status.HTTP_200_OK)
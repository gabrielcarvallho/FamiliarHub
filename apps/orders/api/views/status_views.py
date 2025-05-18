from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.orders.services import StatusService
from apps.orders.api.serializers import StatusSerializer

from apps.core.utils.permissions import UserPermission


class StatusView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = StatusSerializer

    permission_app_label  = 'orders'
    permission_model = 'status'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = StatusService()

    def get(self, request):
        order_status = self.__service.get_all_status()
        response = self.serializer_class(order_status, many=True)

        return Response({'order_status': response.data}, status=status.HTTP_200_OK)
from typing import Any
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.orders.services import OrderService
from apps.orders.api.serializers.order_serializer import OrderRequestSerializer

from apps.core.utils.permissions import UserPermission


class OrderViews(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = OrderRequestSerializer

    permission_app_label  = 'orders'
    permission_model = 'order'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = OrderService()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            order = self.__service.create_order(**serializer.validated_data)
            return Response({'detail': 'ok'}, status=status.HTTP_200_OK)
        
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
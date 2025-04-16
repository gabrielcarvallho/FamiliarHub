from typing import Any
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.core.utils.permissions import UserPermission, IsOwnerOrReadOnly

from apps.orders.services import OrderService
from apps.orders.api.serializers.order_serializer import (
    OrderRequestSerializer, 
    OrderResponseSerializer)


class OrderViews(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = OrderRequestSerializer

    permission_app_label  = 'orders'
    permission_model = 'order'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = OrderService()

    def get(self, request):
        order_id = request.query_params.get('id', None)

        if 'list' in request.GET:
            if request.user.is_admin:
                orders = self.__service.get_all_orders()
                response = OrderResponseSerializer(orders, many=True)

                return Response({'orders': response.data}, status=status.HTTP_200_OK)
            else:
                orders = self.__service.get_orders_by_user(request.user)
                response = OrderResponseSerializer(orders, many=True)

                return Response({'orders': response.data}, status=status.HTTP_200_OK)
            
        if order_id:
            order = self.__service.get_order(order_id)

            if not IsOwnerOrReadOnly().has_object_permission(request, self, order):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            response = OrderResponseSerializer(order)
            return Response({'order': response.data}, status=status.HTTP_200_OK)
        
        return Response({'detail': "Customer ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            self.__service.create_order(request, **serializer.validated_data)
            return Response({'order': 'ok'}, status=status.HTTP_200_OK)
        
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
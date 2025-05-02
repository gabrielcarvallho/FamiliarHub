from typing import Any
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.core.utils.pagination import CustomPagination
from apps.orders.utils.order_permissions import OrderPermission
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
            paginator = CustomPagination()

            if request.user.is_admin:
                orders = self.__service.get_all_orders()
                page = paginator.paginate_queryset(orders, request)

                response = OrderResponseSerializer(page, many=True)
                return paginator.get_paginated_response(response.data, resource_name='orders')
            else:
                orders = self.__service.get_orders_by_user(request.user)
                page = paginator.paginate_queryset(orders, request)

                response = OrderResponseSerializer(page, many=True)
                return paginator.get_paginated_response(response.data, resource_name='orders')
            
        if order_id:
            order = self.__service.get_order(order_id)

            if not IsOwnerOrReadOnly().has_object_permission(request, self, order):
                if not OrderPermission().has_object_permission(request, self, order):
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
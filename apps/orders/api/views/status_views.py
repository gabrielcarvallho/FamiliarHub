from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.orders.services import StatusService
from apps.orders.api.serializers import StatusSerializer, CreateStatusSerializer, UpdateStatusSerializer

from apps.core.utils.permissions import UserPermission


class StatusView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]

    permission_app_label  = 'orders'
    permission_model = 'status'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = StatusService()
    
    def get(self, request):
        delivery_method = request.query_params.get('delivery_method')

        if delivery_method:
            statuses = self.__service.get_status_by_delivery_method(delivery_method)
            response = StatusSerializer(statuses, many=True)

            return Response({'status': response.data}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Delivery method is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = CreateStatusSerializer(data=request.data)

        if serializer.is_valid():
            self.__service.create_status(**serializer.validated_data)
            return Response({'detail': 'Status created successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        status_id = request.data.get('id')

        if status_id:
            statuses = self.__service.get_status(status_id)
            serializer = UpdateStatusSerializer(instance=statuses, data=request.data)

            if serializer.is_valid():
                self.__service.update_status(statuses, **serializer.validated_data)

                return Response({'product': 'Status updated successfully.'}, status=status.HTTP_200_OK)

            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        status_id = request.query_params.get('id', None)

        if status_id:
            self.__service.delete_status(status_id)
            return Response({'detail': 'Status deleted successfully.'}, status=status.HTTP_200_OK)
            
        return Response({'detail': 'Status ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.stock.services import StockConfigurationService
from apps.stock.api.serializers import StockConfigurationSerializer, CreateStockConfigurationSerializer, UpdateStockConfigurationSerializer

from apps.core.utils.permissions import UserPermission
from apps.core.utils.pagination import CustomPagination


class StockConfigurationView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]

    permission_app_label  = 'stock'
    permission_model = 'stockconfiguration'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = StockConfigurationService()
    
    def get(self, request):
        configuration_id = request.query_params.get('id', None)

        if 'list' in request.GET:
            configurations = self.__service.get_all_configurations()

            paginator = CustomPagination()
            page = paginator.paginate_queryset(configurations, request)

            response = StockConfigurationSerializer(page, many=True)
            return paginator.get_paginated_response(response.data, resource_name='stock_configurations')
        
        if configuration_id:
            product = self.__service.get_configuration(configuration_id)
            response = StockConfigurationSerializer(product)

            return Response({'stock_configuration': response.data}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Stock configuration ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = CreateStockConfigurationSerializer(data=request.data)

        if serializer.is_valid():
            self.__service.create_configuration(**serializer.validated_data)
            return Response({'detail': 'Product stock configuration created successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        configuration_id = request.data.get('id')

        if configuration_id:
            configuration = self.__service.get_configuration(configuration_id)
            serializer = UpdateStockConfigurationSerializer(instance=configuration, data=request.data)

            if serializer.is_valid():
                self.__service.update_configuration(configuration, **serializer.validated_data)

                return Response({'product': 'Product stock configuration updated successfully.'}, status=status.HTTP_200_OK)
            
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': 'Stock configuration ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
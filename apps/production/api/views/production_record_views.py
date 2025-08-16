from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.utils.pagination import CustomPagination
from apps.production.services import ProductionRecordService
from apps.production.api.serializers import CreateProductionRecordSerializer, UpdateProductionRecordSerializer, ProductionRecordSerializer

from apps.core.utils.permissions import UserPermission


class ProductionRecordView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]

    permission_app_label  = 'production'
    permission_model = 'productionrecord'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = ProductionRecordService()
    
    def get(self, request):
        record_id = request.query_params.get('id', None)

        if 'list' in request.GET:
            paginator = CustomPagination()

            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)

            production_records = self.__service.get_all_records(start_date, end_date)
            page = paginator.paginate_queryset(production_records, request)

            response = ProductionRecordSerializer(page, many=True)
            return paginator.get_paginated_response(response.data, resource_name='production_records')

        if record_id:
            production_record = self.__service.get_record(record_id)
            response = ProductionRecordSerializer(production_record)

            return Response({'production_record': response.data}, status=status.HTTP_200_OK)

        return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = CreateProductionRecordSerializer(data=request.data)

        if serializer.is_valid():
            self.__service.create_record(request, **serializer.validated_data)
            return Response({'detail': 'Production record created successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        record_id = request.data.get('id')

        if record_id:
            production_record = self.__service.get_record(record_id)
            serializer = UpdateProductionRecordSerializer(instance=production_record, data=request.data)

            if serializer.is_valid():
                self.__service.update_record(production_record, **serializer.validated_data)

                return Response({'product': 'Production record updated successfully.'}, status=status.HTTP_200_OK)
            
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Record ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        record_id = request.query_params.get('id', None)

        if record_id:
            self.__service.delete_record(record_id)
            return Response({'detail': 'Production record deleted successfully.'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Production record ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
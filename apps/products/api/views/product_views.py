from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.products.services import ProductService
from apps.products.api.serializers import ProductSerializer, CreateProductSerializer, UpdateProductSerializer

from apps.core.utils.permissions import UserPermission
from apps.core.utils.pagination import CustomPagination


class ProductView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]

    permission_app_label  = 'products'
    permission_model = 'product'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = ProductService()

    def get(self, request):
        product_id = request.query_params.get('id', None)
        status_filter = request.query_params.get('status')

        if 'list' in request.GET:
            if status_filter == 'active':
                products = self.__service.get_active_products()
            elif status_filter == 'inactive':
                products = self.__service.get_inactive_products()
            elif status_filter == 'all':
                products = self.__service.get_all_products()
            else:
                return Response({'detail': 'Invalid product status.'}, status=status.HTTP_400_BAD_REQUEST)

            paginator = CustomPagination()
            page = paginator.paginate_queryset(products, request)

            response = ProductSerializer(page, many=True)
            return paginator.get_paginated_response(response.data, resource_name='products')
        
        if product_id:
            product = self.__service.get_product(product_id)
            response = ProductSerializer(product)

            return Response({'product': response.data}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)

        if serializer.is_valid():
            self.__service.create_product(**serializer.validated_data)
            return Response({'detail': 'Product created successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        product_id = request.data.get('id')

        if product_id:
            product = self.__service.get_product(product_id)
            serializer = UpdateProductSerializer(instance=product, data=request.data)

            if serializer.is_valid():
                self.__service.update_product(product, **serializer.validated_data)

                return Response({'product': 'Product updated successfully.'}, status=status.HTTP_200_OK)
            
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        product_id = request.query_params.get('id', None)

        if product_id:
            self.__service.delete_product(product_id)
            return Response({'detail': 'Product deleted successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
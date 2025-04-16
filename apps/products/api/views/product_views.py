from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.products.services import ProductService
from apps.products.api.serializers import ProductSerializer

from apps.core.utils.permissions import UserPermission


class ProductView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = ProductSerializer

    permission_app_label  = 'products'
    permission_model = 'product'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = ProductService()

    def get(self, request):
        product_id = request.query_params.get('id', None)

        if 'list' in request.GET:
            products = self.__service.get_all_products()
            response = self.serializer_class(products, many=True)

            return Response({'products': response.data}, status=status.HTTP_200_OK)
        
        if product_id:
            product = self.__service.get_product(product_id)
            response = self.serializer_class(product)

            return Response({'product': response.data}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            product = self.__service.create_product(**serializer.validated_data)
            response = self.serializer_class(product)

            return Response({'product': response.data}, status=status.HTTP_200_OK)
        
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        product_id = request.data.get('id')

        if product_id:
            product = self.__service.get_product(product_id)
            serializer = self.serializer_class(instance=product, data=request.data, partial=True)

            if serializer.is_valid():
                updated_product = self.__service.update_product(product, **serializer.validated_data)
                response = self.serializer_class(updated_product)

                return Response({'product': response.data}, status=status.HTTP_200_OK)
            
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        product_id = request.query_params.get('id', None)

        if product_id:
            self.__service.delete_product(product_id)
            return Response({'detail': 'Product deleted successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
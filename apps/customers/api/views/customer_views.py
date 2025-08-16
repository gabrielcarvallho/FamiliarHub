from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.utils.pagination import CustomPagination
from apps.core.utils.permissions import UserPermission, IsOwnerOrReadOnly

from apps.customers.services import CustomerService
from apps.customers.api.serializers import CreateCustomerSerializer, UpdateCustomerSerializer, CustomerSerializer


class CustomerView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]

    permission_app_label  = 'customers'
    permission_model = 'customer'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = CustomerService()

    def get(self, request):
        customer_id = request.query_params.get('id', None)

        if 'list' in request.GET:
            paginator = CustomPagination()

            customers = self.__service.get_all_customers()
            page = paginator.paginate_queryset(customers, request)
            
            response = CustomerSerializer(page, many=True)
            return paginator.get_paginated_response(response.data, resource_name='customers')
        
        if customer_id:
            customer = self.__service.get_customer(customer_id)

            response = CustomerSerializer(customer)
            return Response({'customer': response.data}, status=status.HTTP_200_OK)
        
        return Response({'detail': "Customer ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = CreateCustomerSerializer(data=request.data)

        if serializer.is_valid():
            self.__service.create_customer(request, **serializer.validated_data)
            return Response({'detail': 'Customer created successfully.'}, status=status.HTTP_201_CREATED)

        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        customer_id = request.data.get('id')

        if customer_id:
            customer = self.__service.get_to_update(customer_id)

            if not IsOwnerOrReadOnly().has_object_permission(request, self, customer):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = UpdateCustomerSerializer(instance=customer, data=request.data)
            if serializer.is_valid():
                self.__service.update_customer(customer, **serializer.validated_data)
                return Response({'detail': 'Customer updated successfully.'}, status=status.HTTP_200_OK)

            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'detail': 'Customer ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        customer_id = request.query_params.get('id', None)

        if customer_id:
            self.__service.delete_customer(customer_id)
            return Response({'detail': 'Customer deleted successfully.'}, status=status.HTTP_200_OK)
            
        return Response({'detail': 'Customer ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
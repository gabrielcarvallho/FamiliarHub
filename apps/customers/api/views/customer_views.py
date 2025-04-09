from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.utils.permissions import UserPermission

from apps.customers.services import CustomerService
from apps.customers.api.serializers import CustomerSerializer


class CustomerView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = CustomerSerializer

    permission_app_label  = 'customers'
    permission_model = 'customer'

    service = CustomerService()

    def get(self, request):
        customer_id = request.query_params.get('id', None)

        if 'list' in request.GET:
            customers = self.service.get_all_customers()
            response = self.serializer_class(customers, many=True)

            return Response({'customers': response.data}, status=status.HTTP_200_OK)
        
        if customer_id:
            customer = self.service.get_customer(customer_id)
            response = self.serializer_class(customer)

            return Response({'customer': response.data}, status=status.HTTP_200_OK)
        
        return Response({'detail': "Customer ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            customer = self.service.create_customer(**serializer.validated_data)
            response = self.serializer_class(customer)

            return Response({'customer': response.data}, status=status.HTTP_200_OK)

        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        customer_id = request.data.get('id')

        if customer_id:
            customer = self.service.get_customer(customer_id)
            serializer = self.serializer_class(instance=customer, data=request.data, partial=True)

            if serializer.is_valid():
                updated_customer = self.service.update_customer(customer, **serializer.validated_data)
                response = self.serializer_class(updated_customer)

                return Response({'customer': response.data}, status=status.HTTP_200_OK)
            
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Customer ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        customer_id = request.query_params.get('id', None)

        if customer_id:
            self.service.delete_customer(customer_id)
            return Response({'detail': 'Customer deleted successfully.'}, status=status.HTTP_200_OK)
            
        return Response({'detail': 'Customer ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.orders.services import PaymentService
from apps.orders.api.serializers import PaymentSerializer, CreatePaymentSerializer, UpdatePaymentSerializer

from apps.core.utils.permissions import UserPermission


class PaymentView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]

    permission_app_label  = 'orders'
    permission_model = 'payment'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = PaymentService()
    
    def get(self, request):
        payment_methods = self.__service.get_all_payment_methods()
        response = PaymentSerializer(payment_methods, many=True)

        return Response({'payment_methods': response.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)

        if serializer.is_valid():
            self.__service.create_payment_method(**serializer.validated_data)
            return Response({'detail': 'Payment method created successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        payment_method_id = request.data.get('id')

        if payment_method_id:
            payment_method = self.__service.get_payment_method(payment_method_id)
            serializer = UpdatePaymentSerializer(instance=payment_method, data=request.data)

            if serializer.is_valid():
                self.__service.update_payment_method(payment_method, **serializer.validated_data)
                return Response({'detail': 'Payment method updated successfully.'}, status=status.HTTP_200_OK)
            
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Payment method ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        payment_method_id = request.query_params.get('id', None)

        if payment_method_id:
            self.__service.delete_payment_method(payment_method_id)
            return Response({'detail': 'Payment method deleted successfully.'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Payment method ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
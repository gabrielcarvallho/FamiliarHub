from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.utils.permissions import UserPermission

from apps.customers.services import AddressService
from apps.customers.api.serializers import AddressSerializer


class AddressView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = AddressSerializer

    permission_app_label  = 'customers'
    permission_model = 'address'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = AddressService()

    def patch(self, request):
        address_id = request.data.get('id')

        if address_id:
            address = self.__service.get_address(address_id)
            serializer = self.serializer_class(instance=address, data=request.data, partial=True)

            if serializer.is_valid():
                updated_address = self.__service.update_address(address, **serializer.validated_data)
                response = self.serializer_class(updated_address)

                return Response({'address': response.data}, status=status.HTTP_200_OK)
            
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Address ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        address_id = request.query_params.get('id', None)

        if address_id:
            self.__service.delete_address(address_id)
            return Response({'detail': 'Address deleted successfully.'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Address ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.utils.permissions import UserPermission
from apps.accounts.services import UserInvitationService
from apps.accounts.api.serializers import CustomUserRequestSerializer


class UserInvitationView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = CustomUserRequestSerializer

    permission_app_label  = 'accounts'
    permission_model = 'customuser'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = UserInvitationService()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = self.__service.create_invite(request.user, **serializer.validated_data)
            return Response({'detail': 'User invited successfully.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
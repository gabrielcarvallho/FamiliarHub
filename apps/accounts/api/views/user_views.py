from apps.accounts.api.serializers import (
    CustomUserResponseSerializer, 
    CustomUserRequestSerializer
)

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.utils.permissions import UserPermission
from apps.accounts.services import AuthService, UserService, GroupService


class CustomUserView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = CustomUserRequestSerializer

    permission_app_label  = 'accounts'
    permission_model = 'customuser'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserService()

    def get(self, request):
        user_id = request.query_params.get('id', None)

        if request.query_params.get('list'):
            users = self.service.get_all_users(request)
            serializer = CustomUserResponseSerializer(users, many=True)
            
            return Response({'users': serializer.data}, status=status.HTTP_200_OK)
        
        user = self.service.get_user_by_id(request, user_id)
        serializer = CustomUserResponseSerializer(user)

        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        auth_service = AuthService()

        token = request.query_params.get('token')
        if not token:
            return Response({'detail': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        payload = auth_service.token_decode(token)
        request_data = request.data.copy()

        request_data['is_admin'] = payload.get('is_admin')
        request_data['group'] = payload.get('group')

        serializer = self.serializer_class(data=request_data)

        if serializer.is_valid():
            self.service.create_user(serializer.validated_data)
            return Response({'user': serializer.validated_data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_id = request.query_params.get('id', None)

        if user_id:
            self.service.delete_user(user_id)
            return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

class InviteUserView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = CustomUserRequestSerializer

    permission_app_label  = 'accounts'
    permission_model = 'customuser'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserService()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.service.invite_user(serializer.validated_data)
            return Response({'detail': 'User invited successfully.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, UserPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = GroupService()

    def get(self, request):
        groups = self.service.get_all_groups(request)
        return Response({'groups': groups}, status=status.HTTP_200_OK)
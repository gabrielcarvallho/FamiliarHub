from apps.accounts.api.serializers import CustomUserSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.services import UserService
from apps.core.utils.permissions import UserPermission
from apps.core.utils.pagination import CustomPagination


class CustomUserView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = CustomUserSerializer

    permission_app_label  = 'accounts'
    permission_model = 'customuser'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = UserService()

    def get(self, request):
        user_id = request.query_params.get('id', None)

        if 'list' in request.GET:
            users = self.__service.get_all_users(request)

            paginator = CustomPagination()
            page = paginator.paginate_queryset(users, request)

            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data, resource_name='users')
        
        user = self.__service.get_user(request, user_id)
        serializer = self.serializer_class(user)

        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request):
        user_id = request.query_params.get('id', None)

        if user_id:
            self.__service.delete_user(user_id)
            return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
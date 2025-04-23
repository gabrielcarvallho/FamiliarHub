from apps.accounts.api.serializers import GroupSerializer

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.accounts.services import GroupService
from apps.core.utils.permissions import UserPermission


class GroupListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, UserPermission]
    serializer_class = GroupSerializer

    permission_app_label  = 'accounts'
    permission_model = 'customuser'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = GroupService()

    def get(self, request):
        groups = self.__service.get_all_groups(request)
        response = self.serializer_class(groups, many=True)

        return Response({'groups': response.data}, status=status.HTTP_200_OK)
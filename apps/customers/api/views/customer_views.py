from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.core.utils.permissions import UserPermission


class CustomerView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]

    permission_app_label  = 'customers'
    permission_model = 'customer'
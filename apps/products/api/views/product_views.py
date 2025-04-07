from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.core.utils.permissions import UserPermission


class ProductView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]

    permission_app_label  = 'products'
    permission_model = 'product'

    def get(self, request):
        pass
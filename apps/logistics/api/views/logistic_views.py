from typing import Any
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.core.utils.permissions import UserPermission

from apps.logistics.services import ProductionScheduleService


class LogisticView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]

    permission_app_label  = 'logistics'
    permission_model = 'productionschedule'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__service = ProductionScheduleService()
    
    def get(self, request):
        response = self.__service.get_production()
        return Response({'production_schedule': list(response.values())}, status=status.HTTP_200_OK)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.utils.permissions import UserPermission
from apps.reports.services import ReportService


class ReportView(APIView):
    permission_classes = [IsAuthenticated, UserPermission]

    permission_app_label  = 'reports'
    permission_model = 'report'

    def __init__(self, **kwargs) :
        super().__init__(**kwargs)
        self.__service = ReportService()

    def get(self, request):
        try:
            days = int(request.query_params.get('days', 0))

            response = self.__service.get_reports(days)
            return Response({'report': response}, status=status.HTTP_200_OK)
        except (TypeError, ValueError):
            return Response({'detail': '{days} must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)
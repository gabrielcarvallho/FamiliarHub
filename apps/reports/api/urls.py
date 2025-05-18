from django.urls import path
from apps.reports.api.views import ReportView


urlpatterns = [
    path('', ReportView.as_view(), name='product')
]
from django.urls import path
from apps.production.api.views import ProductionRecordView


urlpatterns = [
    path('', ProductionRecordView.as_view(), name='production_record')
]
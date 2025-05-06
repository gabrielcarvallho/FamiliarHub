from django.urls import path
from apps.logistics.api.views import LogisticView


urlpatterns = [
    path('', LogisticView.as_view(), name='order'),
]
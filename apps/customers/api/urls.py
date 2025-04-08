from django.urls import path
from apps.customers.api.views import CustomerView


urlpatterns = [
    path('', CustomerView.as_view(), name='customer')
]
from django.urls import path
from apps.customers.api.views import CustomerView, AddressView


urlpatterns = [
    path('', CustomerView.as_view(), name='customer'),
    path('address/', AddressView.as_view(), name='customer_address')
]
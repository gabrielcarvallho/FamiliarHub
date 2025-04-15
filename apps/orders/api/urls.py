from django.urls import path
from apps.orders.api.views import PaymentView, StatusView


urlpatterns = [
    path('payment-methods/', PaymentView.as_view(), name='order_payment_methods'),
    path('status/', StatusView.as_view(), name='order_status')
]
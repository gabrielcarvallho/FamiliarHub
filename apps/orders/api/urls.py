from django.urls import path
from apps.orders.api.views import PaymentView


urlpatterns = [
    path('payment-methods/', PaymentView.as_view(), name='order_payment_methods')
]
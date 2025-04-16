from django.urls import path
from apps.orders.api.views import OrderViews, StatusView, PaymentView


urlpatterns = [
    path('', OrderViews.as_view(), name='order'),
    path('payment-methods/', PaymentView.as_view(), name='order_payment_methods'),
    path('status/', StatusView.as_view(), name='order_status')
]
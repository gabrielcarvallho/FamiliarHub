from django.urls import path
from apps.stock.api.views import StockConfigurationView


urlpatterns = [
    path('', StockConfigurationView.as_view(), name='stock_configuration')
]
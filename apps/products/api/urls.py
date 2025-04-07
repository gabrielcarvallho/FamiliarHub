from django.urls import path
from apps.products.api.views import ProductView


urlpatterns = [
    path('', ProductView.as_view(), name='product')
]
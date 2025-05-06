from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/accounts/', include('apps.accounts.api.urls')),
    path('api/customers/', include('apps.customers.api.urls')),
    path('api/products/', include('apps.products.api.urls')),
    path('api/orders/', include('apps.orders.api.urls')),
    path('api/logistic/', include('apps.logistics.api.urls'))
]
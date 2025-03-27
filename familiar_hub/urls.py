from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/accounts/', include('apps.accounts.api.urls')),
]
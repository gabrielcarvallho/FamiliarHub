from django.urls import path
from apps.core.api.views import get_cep


urlpatterns = [
    path('get-cep/', get_cep, name='get_cep')
]
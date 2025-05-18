from django.urls import path
from apps.core.api.views import get_cep, get_cnpj


urlpatterns = [
    path('get-cep/', get_cep, name='get_cep'),
    path('get-cnpj/', get_cnpj, name='get_cnpj')
]
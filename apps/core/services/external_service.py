import re
from django.conf import settings

from rest_framework.exceptions import ValidationError

from apps.core.utils.http_client import HttpClient
from apps.core.services.base_service import ServiceBase


class ExternalService(metaclass=ServiceBase):
    def __init__(self):
        self._http_client = HttpClient(base_timeout=10)

    def request_cep_api(self, cep):
        cep = self._validate_cep(cep)

        api_url = f'{settings.CEP_API_URL}/{cep}/json/'
        response = self._http_client.get(
            api_url, 
            resource_type="CEP",
            resource_value=cep
        )

        if response.get('erro'):
            raise ValidationError(f'CEP {cep} not found.')
                
        return response
    
    def request_cnpj_api(self, cnpj):
        cnpj = self._validate_cnpj(cnpj)

        api_url = f'{settings.CNPJ_API_URL}/{cnpj}'
        headers = {
            'Authorization': f'Bearer {settings.CNPJ_API_KEY}'
        }

        response = self._http_client.get(
            api_url,
            headers=headers
        )

        if response.get('status') == 'ERROR':
            raise ValidationError(f'Request error: {response.get('message')}')

        return response

    def _validate_cep(self, cep):
        cep = cep.replace('-', '').replace('.', '').replace(' ', '')

        if len(cep) != 8:
            raise ValidationError('CEP must have 8 digits.')
        
        return cep
    
    def _validate_cnpj(self, cnpj):
        cnpj = re.sub(r'\D', '', cnpj)

        if len(cnpj) != 14:
            raise ValidationError('CNPJ must have 14 digits.')
        
        return cnpj
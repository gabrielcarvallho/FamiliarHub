from .base_service import ServiceBase
from apps.core.utils.http_client import HttpClient

from rest_framework.exceptions import ValidationError


class ExternalService(metaclass=ServiceBase):
    def __init__(self):
        self._http_client = HttpClient(base_timeout=10)

    def request_cep_api(self, cep):
        cep = self._validate_cep(cep)

        url = f'https://viacep.com.br/ws/{cep}/json/'
        
        data = self._http_client.get(
            url, 
            resource_type="CEP",
            resource_value=cep
        )

        if data.get('erro'):
            raise ValidationError(f'CEP {cep} not found.')
                
        return data

    def _validate_cep(self, cep):
        cep = cep.replace('-', '').replace('.', '').replace(' ', '')

        if len(cep) != 8:
            raise ValidationError('CEP must have 8 digits.')
        
        return cep
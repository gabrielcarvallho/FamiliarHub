import requests
from rest_framework.exceptions import ValidationError


class HttpClient:
    def __init__(self, base_timeout=10):
        self.base_timeout = base_timeout
    
    def request(self, method, url, headers=None, params=None, data=None, json=None, timeout=None, resource_type=None, resource_value=None):
        timeout = timeout or self.base_timeout
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                timeout=timeout
            )
            response.raise_for_status()

            return response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                
        except requests.exceptions.RequestException as e:
            error_msg = {
                requests.exceptions.Timeout: 'The request timed out.',
                requests.exceptions.ConnectionError: 'Failed to connect to the server.',
            }.get(type(e), f'Request error: {str(e)}')

            if isinstance(e, requests.exceptions.HTTPError):
                if response.status_code == 404 and resource_type and resource_value:
                    error_msg = f'{resource_type} {resource_value} was not found.'
                elif response.status_code == 401:
                    error_msg = 'Unauthorized. Please check your credentials.'
            
            raise ValidationError(error_msg)
    
    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)
    
    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)
    
    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)
    
    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)
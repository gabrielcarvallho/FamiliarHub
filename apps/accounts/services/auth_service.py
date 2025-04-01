import jwt
from datetime import timedelta
from django.conf import settings

from apps.core.services.base_service import ServiceBase

from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class AuthService(metaclass=ServiceBase):
    def logout(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            raise AuthenticationFailed('No refresh token provided.')
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as e:
            raise AuthenticationFailed('Invalid refresh token.')
    
    def token_decode(self, token):
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.InvalidSignatureError:
            raise AuthenticationFailed('Invalid token signature.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')

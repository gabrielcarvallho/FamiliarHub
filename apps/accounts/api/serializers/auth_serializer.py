from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email

        return token
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid credentials.')
        
        data = super().validate(attrs)

        data['user'] = {
            'id': user.id,
            'email': user.email,
            'is_admin': user.is_admin,
            'group_id': user.groups.first().id if user.groups.exists() else None
        }

        return data
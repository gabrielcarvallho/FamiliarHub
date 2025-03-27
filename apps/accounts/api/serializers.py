from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.accounts.models import CustomUser, Group


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
        
        return super().validate(attrs)

class CustomUserRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(
            queryset=CustomUser.objects.all(), 
            message="This email is already in use."
        )]
    )
    
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        min_length=8
    )

    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False,
        error_messages={
            'does_not_exist': 'Group not found.'
        }
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_admin', 'group']

    def validate(self, attrs):
        is_admin = attrs.get('is_admin', False)
        group = attrs.get('group')
        
        if not is_admin and not group:
            raise serializers.ValidationError({"group": "A group is required when is_admin is False."})
            
        return attrs

class CustomUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_admin', 'date_joined', 'groups']
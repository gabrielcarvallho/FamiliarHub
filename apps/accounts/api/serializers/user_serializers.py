from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.accounts.models import CustomUser, Group


class CustomUserRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
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
        allow_null=True,
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
        
        if is_admin and group:
            raise serializers.ValidationError({"group": "Group is not allowed for admin users."})

        return attrs

class CustomUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_admin', 'date_joined', 'groups']
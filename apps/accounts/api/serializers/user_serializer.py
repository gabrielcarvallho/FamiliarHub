from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.accounts.models import CustomUser, Group
from apps.accounts.api.serializers import GroupSerializer


class CustomUserRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        min_length=8
    )

    group_id = serializers.IntegerField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_admin', 'group_id']

    def validate(self, attrs):
        is_admin = attrs.get('is_admin', False)
        group_id = attrs.get('group_id')
        
        if not is_admin and not group_id:
            raise serializers.ValidationError({"group_id": "A group is required when is_admin is False."})
        
        if is_admin and group_id:
            raise serializers.ValidationError({"group_id": "Group is not allowed for admin users."})

        return attrs

class CustomUserResponseSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_admin', 'date_joined', 'groups']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        ordered_data = {
            'id': representation.get('id'),
            'email': representation.get('email'),
            'is_admin': representation.get('is_admin'),
            'date_joined': representation.get('date_joined'),
            'groups': representation.get('groups'),

        }

        return ordered_data
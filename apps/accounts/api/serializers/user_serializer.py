from rest_framework import serializers

from apps.accounts.models import CustomUser
from apps.accounts.api.serializers import GroupSerializer


class CustomUserSerializer(serializers.ModelSerializer):
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
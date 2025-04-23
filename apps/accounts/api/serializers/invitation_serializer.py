from rest_framework import serializers
from apps.accounts.models import CustomUserInvitation


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserInvitation
        fields = ['id', 'email', 'token', 'accepted', 'created_at', 'expire_at']
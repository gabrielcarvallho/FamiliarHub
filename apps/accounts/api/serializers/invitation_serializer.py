from rest_framework import serializers
from apps.accounts.models import CustomUserInvitation


class InvitationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    is_admin = serializers.BooleanField(default=False)
    group_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        is_admin = attrs.get('is_admin')
        group_id = attrs.get('group_id', None)
        
        if not is_admin and not group_id:
            raise serializers.ValidationError({"group_id": "A group is required when is_admin is False."})
        
        if is_admin and (group_id or group_id == 0):
            raise serializers.ValidationError({"group_id": "Group is not allowed for admin users."})

        return attrs

class InvitationAcceptedRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, min_length=8)
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'}, min_length=8)

class InvitationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserInvitation
        fields = ['id', 'email', 'token', 'accepted', 'created_at', 'expire_at']
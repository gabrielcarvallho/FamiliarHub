from apps.orders.models import Payment
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CreatePaymentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    is_requires_due_date = serializers.BooleanField(default=False)

class UpdatePaymentSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=20)
    is_requires_due_date = serializers.BooleanField(default=False)
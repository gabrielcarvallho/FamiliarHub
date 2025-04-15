from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.orders.models import Order
from apps.customers.api.serializers import AddressSerializer, CustomerSerializer

from apps.orders.api.serializers import (
    StatusSerializer,
    PaymentSerializer,
    ProductOrderSerializer
)


class OrderRequestSerializer(serializers.Serializer):
    customer_id = serializers.UUIDField(format='hex_verbose', write_only=True)
    order_status_id = serializers.UUIDField(format='hex_verbose', write_only=True)
    payment_method_id = serializers.UUIDField(format='hex_verbose', write_only=True)
    delivery_date = serializers.DateField()

    delivery_address_id = serializers.UUIDField(required=False)
    delivery_address = AddressSerializer(required=False)

    products = ProductOrderSerializer(many=True)

    def validate(self, attrs):
        if 'delivery_address_id' not in attrs and 'delivery_address' not in attrs:
            raise serializers.ValidationError("'delivery_address_id' or 'delivery_address' must be provided.")
        
        if 'delivery_address_id' in attrs and 'delivery_address' in attrs:
            raise serializers.ValidationError("Provide 'delivery_address_id' or 'delivery_address', not both.")
        
        if 'products' not in attrs or not attrs['products']:
            raise serializers.ValidationError("Order must have at least one product.")
        
        today = timezone.now().date()
        delivery_date = attrs.get('delivery_date')

        if delivery_date < today:
            raise serializers.ValidationError("Invalid delivery date.")
        
        return attrs
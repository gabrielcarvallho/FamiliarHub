from django.utils import timezone
from rest_framework import serializers

from apps.orders.models import Order
from apps.customers.api.serializers import AddressSerializer, CustomerCustomSerializer

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

class OrderResponseSerializer(serializers.ModelSerializer):
    customer = CustomerCustomSerializer()
    order_status = StatusSerializer()
    payment_method = PaymentSerializer()
    delivery_address = AddressSerializer()
    products = ProductOrderSerializer(many=True, source='product_items')

    class Meta:
        model = Order
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        ordered_data = {
            'id': representation.get('id'),
            'customer': representation.get('customer'),
            'products': representation.get('products'),
            'total_price': f"{instance.total_price:.2f}",
            'payment_method': representation.get('payment_method'),
            'delivery_address': representation.get('delivery_address'),
            'delivery_date': representation.get('delivery_date'),
            'due_date': instance.payment_due_date,
            'order_status': representation.get('order_status'),
            'created_at': representation.get('created_at'),
            'updated_at': representation.get('updated_at'),
        }

        return ordered_data
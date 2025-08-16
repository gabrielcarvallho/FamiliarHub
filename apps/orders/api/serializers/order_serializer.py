from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import APIException

from apps.orders.models import Order
from apps.orders.enums import DeliveryMethod
from apps.orders.utils.fields import DateField
from apps.customers.api.serializers import AddressSerializer

from apps.orders.api.serializers import (
    StatusSerializer,
    PaymentSerializer,
    ProductOrderSerializer
)


class OrderCustomerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    
class OrderRequestSerializer(serializers.Serializer):
    customer_id = serializers.UUIDField(format='hex_verbose', write_only=True)
    order_status_id = serializers.UUIDField(format='hex_verbose', write_only=True)
    payment_method_id = serializers.UUIDField(format='hex_verbose', write_only=True)
    payment_due_days = serializers.IntegerField(required=False)

    delivery_method = serializers.ChoiceField(choices=DeliveryMethod.choices)
    delivery_date = DateField()

    delivery_address_id = serializers.UUIDField(required=False)
    delivery_address = AddressSerializer(required=False)

    is_delivered = serializers.BooleanField(required=False)

    products = ProductOrderSerializer(many=True)
    table_order = serializers.IntegerField(required=False)

    def validate(self, attrs):
        context = self.context.get('action')
        
        if context == 'create':
            delivery_method = attrs.get('delivery_method')
            if delivery_method == 'ENTREGA':
                if 'delivery_address_id' not in attrs and 'delivery_address' not in attrs:
                    raise APIException("'delivery_address_id' or 'delivery_address' must be provided.")
            
            if 'products' not in attrs or not attrs['products']:
                raise APIException("Order must have at least one product.")
        
            if 'delivery_address_id' in attrs and 'delivery_address' in attrs:
                raise APIException("Provide 'delivery_address_id' or 'delivery_address', not both.")
            
            is_delivered = attrs.get('is_delivered', None)
            if is_delivered:
                raise APIException("Cannot mark an order as delivered during creation.")
        
        today = timezone.now().date()
        delivery_date = attrs.get('delivery_date', None)

        if delivery_date and delivery_date < today:
            raise APIException("Invalid delivery date.")
        
        return attrs

class OrderResponseSerializer(serializers.ModelSerializer):
    customer = OrderCustomerSerializer()
    order_status = StatusSerializer()
    payment_method = PaymentSerializer()
    delivery_address = AddressSerializer(required=False)
    products = ProductOrderSerializer(many=True, source='product_items')

    class Meta:
        model = Order
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        ordered_data = {
            'id': representation.get('id'),
            'order_number': representation.get('order_number'),
            'customer': representation.get('customer'),
            'products': representation.get('products'),
            'total_price': f"{instance.total_price:.2f}",
            'payment_method': representation.get('payment_method'),
            'delivery_date': representation.get('delivery_date'),
            'delivery_method': representation.get('delivery_method'),
            'delivery_address': representation.get('delivery_address'),
            'is_delivered': representation.get('is_delivered'),
            'due_date': instance.payment_due_date,
            'order_status': representation.get('order_status'),
            'created_at': representation.get('created_at'),
            'updated_at': representation.get('updated_at'),
            'table_order': representation.get('table_order')
        }

        return ordered_data

class WorkSerializer(serializers.Serializer):
    order_ids = serializers.ListField(
        child=serializers.UUIDField(format='hex_verbose', write_only=True)
    )
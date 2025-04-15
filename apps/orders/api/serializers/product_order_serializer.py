from rest_framework import serializers

from apps.orders.models import ProductOrder
from apps.products.api.serializers import ProductSerializer


class ProductOrderSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(format='hex_verbose', write_only=True)

    class Meta:
        model = ProductOrder
        fields = ['id', 'product_id', 'quantity']
        read_only_fields = ['id']
    
    def validate(self, attrs):
        quantity = attrs.get('quantity')

        if quantity <= 0:
            raise serializers.ValidationError('Quantity cannot be less than or equal to zero')
        
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        ordered_data = {
            'id': representation.get('id'),
            'product': ProductSerializer(instance.product).data,
            'quantity': representation.get('quantity'),
            'total_price': instance.total_price
        }

        return ordered_data
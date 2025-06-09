from rest_framework import serializers

from apps.orders.models import ProductOrder
from apps.products.api.serializers import ProductSerializer


class ProductOrderSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(format='hex_verbose', write_only=True)

    class Meta:
        model = ProductOrder
        fields = ['id', 'product_id', 'quantity', 'sale_price']
        read_only_fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        ordered_data = {
            'id': representation.get('id'),
            'product': ProductSerializer(instance.product).data,
            'quantity': representation.get('quantity'),
            'sale_price': representation.get('sale_price'),
            'total_price': f"{instance.total_price:.2f}"
        }

        return ordered_data
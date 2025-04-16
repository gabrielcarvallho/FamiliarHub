from decimal import Decimal
from rest_framework import serializers
from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        ordered_data = {
            'id': representation.get('id'),
            'name': representation.get('name'),
            'price': representation.get('price'),
            'weight': f"{representation.get('weight')}g",
            'batch_packages': representation.get('batch_packages'),
            'batch_per_days': representation.get('batch_per_days'),
            'production_days': representation.get('production_days'),
            'created_at': representation.get('created_at'),
            'updated_at': representation.get('updated_at')
        }

        return ordered_data
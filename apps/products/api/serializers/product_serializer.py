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
        data = super().to_representation(instance)

        ordered_data = {
            'id': data.get('id'),
            'name': data.get('name'),
            'price': data.get('price'),
            'weight': data.get('weight'),
            'batch_packages': data.get('batch_packages'),
            'created_at': data.get('created_at'),
            'updated_at': data.get('updated_at')
        }

        return ordered_data
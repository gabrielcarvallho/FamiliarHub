from rest_framework import serializers
from rest_framework.validators import ValidationError

from apps.stock.api.serializers import StockConfigurationSerializer


class ProductSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)

    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    
class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)

    def validate(self, attrs):
        price = attrs['price']
        weight = attrs['weight']

        if price <= 0:
            raise ValidationError('Price must be greater than 0.')
        
        if weight <= 0:
            raise ValidationError('Weight must be greater than 0.')

        return attrs

class UpdateProductSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)

    def validate(self, attrs):
        price = attrs['price']
        weight = attrs['weight']

        if price <= 0:
            raise ValidationError('Price must be greater than 0.')
        
        if weight <= 0:
            raise ValidationError('Weight must be greater than 0.')
        
        return attrs
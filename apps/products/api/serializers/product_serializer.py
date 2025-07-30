from rest_framework import serializers
from rest_framework.validators import ValidationError


class ProductSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    current_stock = serializers.IntegerField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    
class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    current_stock = serializers.IntegerField(default=0)

    def validate(self, attrs):
        current_stock = attrs['current_stock']
        weight = attrs['weight']
        price = attrs['price']

        if current_stock < 0:
            raise ValidationError('Current stock cannot be less than 0.')
        
        if weight <= 0:
            raise ValidationError('Weight must be greater than 0.')
        
        if price <= 0:
            raise ValidationError('Price must be greater than 0.')
        
        return attrs

class UpdateProductSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    current_stock = serializers.IntegerField(default=0)

    def validate(self, attrs):
        current_stock = attrs['current_stock']
        weight = attrs['weight']
        price = attrs['price']

        if current_stock < 0:
            raise ValidationError('Current stock cannot be less than 0.')
        
        if weight <= 0:
            raise ValidationError('Weight must be greater than 0.')
        
        if price <= 0:
            raise ValidationError('Price must be greater than 0.')
        
        return attrs
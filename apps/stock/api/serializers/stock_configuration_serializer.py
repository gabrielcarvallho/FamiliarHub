from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.stock.models import StockConfiguration


class StockConfigurationSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(source='product.id', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = StockConfiguration
        fields = [
            'id',
            'product_id',
            'product_name',
            'current_stock',
            'min_stock_threshold',
            'max_stock_capacity',
            'is_active',
            'updated_at'
        ]

class CreateStockConfigurationSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    current_stock = serializers.IntegerField()
    min_stock_threshold = serializers.IntegerField()
    max_stock_capacity = serializers.IntegerField()

    def validate(self, attrs):
        current_stock = attrs['current_stock']
        min_stock_threshold = attrs['min_stock_threshold']
        max_stock_capacity = attrs['max_stock_capacity']

        if current_stock < 0:
            raise ValidationError('Current stock cannot be less than 0.')
        
        if min_stock_threshold < 0:
            raise ValidationError('Min stock threshold cannot be less than 0.')
        
        if max_stock_capacity < 0:
            raise ValidationError('Max stock capacity cannot be less than 0.')

        return attrs

class UpdateStockConfigurationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    current_stock = serializers.IntegerField()
    min_stock_threshold = serializers.IntegerField()
    max_stock_capacity = serializers.IntegerField()

    def validate(self, attrs):
        current_stock = attrs['current_stock']
        min_stock_threshold = attrs['min_stock_threshold']
        max_stock_capacity = attrs['max_stock_capacity']

        if current_stock < 0:
            raise ValidationError('Current stock cannot be less than 0.')
        
        if min_stock_threshold < 0:
            raise ValidationError('Min stock threshold cannot be less than 0.')
        
        if max_stock_capacity < 0:
            raise ValidationError('Max stock capacity cannot be less than 0.')

        return attrs
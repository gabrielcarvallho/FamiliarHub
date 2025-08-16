from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.production.models import ProductionItem


class ProductionItemRequestSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity_produced = serializers.IntegerField()
    expiration_date = serializers.DateField(required=False, allow_null=True)

    def validate(self, attrs):
        quantity = attrs.get('quantity_produced')

        if quantity <= 0:
            raise ValidationError("Quantity must be greater than 0.")
        
        return attrs

class ProductionItemResponseSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = ProductionItem
        fields = ['id', 'product_id', 'product_name', 'quantity_produced', 'expiration_date']
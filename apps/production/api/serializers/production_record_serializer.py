from rest_framework import serializers
from apps.production.enums import ProductionStatus
from apps.production.api.serializers import ProductionItemRequestSerializer, ProductionItemResponseSerializer

from apps.production.models import ProductionRecord


class ProductionRecordSerializer(serializers.ModelSerializer):
    production_items = ProductionItemResponseSerializer(many=True, read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    duration_days = serializers.ReadOnlyField()
    
    class Meta:
        model = ProductionRecord
        fields = ['id', 'start_date', 'end_date', 'status', 'notes', 'created_by_id', 
            'created_by_email', 'created_at', 'updated_at', 'duration_days', 'production_items']

class CreateProductionRecordSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField(required=False, allow_null=True)
    status = serializers.ChoiceField(ProductionStatus.choices)
    notes = serializers.CharField(max_length=200, required=False, allow_blank=True)
    production_items = ProductionItemRequestSerializer(many=True)

class UpdateProductionRecordSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    start_date = serializers.DateField()
    end_date = serializers.DateField(required=False, allow_null=True)
    status = serializers.ChoiceField(ProductionStatus.choices)
    notes = serializers.CharField(max_length=200, required=False, allow_blank=True)
    production_items = ProductionItemRequestSerializer(many=True)
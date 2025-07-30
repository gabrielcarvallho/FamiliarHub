from rest_framework import serializers
from apps.orders.enums import StatusCategory, DeliveryMethod


class StatusSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    description = serializers.CharField(max_length=120)
    category = serializers.ChoiceField(choices=StatusCategory.choices)
    delivery_method = serializers.ChoiceField(choices=DeliveryMethod.choices)
    sequence_order = serializers.IntegerField()

class CreateStatusSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=120)
    category = serializers.ChoiceField(choices=StatusCategory.choices)
    delivery_method = serializers.ChoiceField(choices=DeliveryMethod.choices, required=False, allow_blank=True)
    sequence_order = serializers.IntegerField()

class UpdateStatusSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    description = serializers.CharField(max_length=120)
    category = serializers.ChoiceField(choices=StatusCategory.choices)
    delivery_method = serializers.ChoiceField(choices=DeliveryMethod.choices, required=False, allow_blank=True)
    sequence_order = serializers.IntegerField()
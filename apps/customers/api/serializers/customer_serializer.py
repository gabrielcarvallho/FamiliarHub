from rest_framework import serializers

from apps.customers.utils import fields
from apps.customers.enums import CustomerType
from apps.customers.api.validators import CustomerValidator
from apps.accounts.api.serializers import CustomUserSerializer
from apps.customers.api.serializers import ContactSerializer, AddressSerializer


class CustomerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    customer_type = serializers.ChoiceField(choices=CustomerType.choices)
    document = serializers.CharField()
    name = serializers.CharField()
    fantasy_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = fields.PhoneNumberField()
    email = serializers.EmailField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False)
    state_registration = serializers.CharField(required=False, allow_blank=True)

    contact = ContactSerializer(required=False)
    addresses = AddressSerializer(many=True, required=False)
    billing_address = AddressSerializer(write_only=True)

    created_by = CustomUserSerializer()

    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def to_representation(self, obj):
        representation = super().to_representation(obj)

        if hasattr(obj, 'billing_address') and obj.billing_address:
            representation['billing_address'] = AddressSerializer(obj.billing_address[0]).data
            representation.pop('addresses', None)
        else:
            representation.pop('billing_address', None)

        return representation

class CreateCustomerSerializer(serializers.Serializer):
    customer_type = serializers.ChoiceField(choices=CustomerType.choices)
    document = serializers.CharField()
    name = serializers.CharField()
    fantasy_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = fields.PhoneNumberField()
    email = serializers.EmailField(required=False)
    birth_date = serializers.DateField(required=False, allow_null=True)
    state_registration = serializers.CharField(required=False)
    contact = ContactSerializer(required=False)
    billing_address = AddressSerializer(write_only=True)

    def validate(self, attrs):
        clean_doc = CustomerValidator.validate_document_by_type(
            attrs['customer_type'], 
            attrs['document']
        )

        attrs['document'] = clean_doc        
        return attrs

class UpdateCustomerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    customer_type = serializers.ChoiceField(choices=CustomerType.choices)
    document = serializers.CharField()
    name = serializers.CharField()
    fantasy_name = serializers.CharField(allow_blank=True)
    phone_number = fields.PhoneNumberField()
    email = serializers.EmailField(allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    state_registration = serializers.CharField(allow_blank=True)
    contact = ContactSerializer(required=False)
    billing_address = AddressSerializer(write_only=True)

    def validate(self, attrs):
        clean_doc = CustomerValidator.validate_document_by_type(
            attrs['customer_type'], 
            attrs['document']
        )

        attrs['document'] = clean_doc 
        return attrs
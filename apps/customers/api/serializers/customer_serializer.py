from rest_framework import serializers

from apps.customers.utils import fields
from apps.customers.models import Customer
from apps.accounts.api.serializers import CustomUserResponseSerializer
from apps.customers.api.serializers import ContactSerializer, AddressSerializer

    
class CustomerSerializer(serializers.ModelSerializer):
    cnpj = fields.CNPJField()
    phone_number = fields.PhoneNumberField()
    state_tax_registration = fields.StateTaxField(required=False, allow_blank=True)

    contact = ContactSerializer()
    addresses = AddressSerializer(many=True, required=False)
    billing_address = AddressSerializer(write_only=True)

    created_by = CustomUserResponseSerializer(required=False)

    class Meta:
        model = Customer
        fields = [
            'id', 'company_name', 'brand_name', 'cnpj', 'phone_number', 'email', 
            'state_tax_registration', 'addresses', 'contact', 'billing_address', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'addresses', 'created_by']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        is_list_view = hasattr(instance, 'billing_address')

        if is_list_view and instance.billing_address:
            representation['billing_address'] = AddressSerializer(instance.billing_address[0]).data
            representation.pop('addresses', None)
        else:
            representation.pop('billing_address', None)

        ordered_fields = [
            'id',
            'company_name',
            'brand_name',
            'cnpj',
            'phone_number',
            'email',
            'state_tax_registration',
            'billing_address' if is_list_view else 'addresses',
            'contact',
            'created_by',
            'created_at',
            'updated_at'
        ]

        return {field: representation.get(field) for field in ordered_fields if field in representation}
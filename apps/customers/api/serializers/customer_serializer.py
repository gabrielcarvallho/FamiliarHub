from rest_framework import serializers

from apps.customers.utils import fields
from apps.customers.models import Customer
from apps.customers.api.serializers import ContactSerializer


class CustomerSerializer(serializers.ModelSerializer):
    cnpj = fields.CNPJField()
    phone_number = fields.PhoneNumberField()
    state_tax_registration = fields.StateTaxField(required=False, allow_blank=True)

    contact = ContactSerializer()

    class Meta:
        model = Customer
        fields = [
            'id', 
            'company_name', 
            'brand_name', 
            'cnpj', 
            'phone_number', 
            'email', 
            'state_tax_registration', 
            'contact',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        ordered_data = {
            'id': data.get('id'),
            'company_name': data.get('company_name'),
            'brand_name': data.get('brand_name'),
            'cnpj': data.get('cnpj'),
            'phone_number': data.get('phone_number'),
            'email': data.get('email'),
            'state_tax_registration': data.get('state_tax_registration'),
            'contact': data.get('contact'),
            'created_at': data.get('created_at'),
            'updated_at': data.get('updated_at'),
        }

        return ordered_data
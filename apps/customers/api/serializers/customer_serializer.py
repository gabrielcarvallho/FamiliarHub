from rest_framework import serializers

from apps.customers.models import Customer, CustomerContact
from apps.customers.utils import validate_cnpj, validate_phone, validate_state_tax_registration


class CustomerContactSerializer(serializers.ModelSerializer):
    contact_phone = serializers.CharField(validators=[validate_phone])

    class Meta:
        model = CustomerContact
        fields = [
            'id', 
            'name', 
            'date_of_birth', 
            'contact_phone', 
            'contact_email', 
            'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        ordered_data = {
            'id': data.get('id'),
            'name': data.get('name'),
            'date_of_birth': data.get('date_of_birth'),
            'contact_phone': data.get('contact_phone'),
            'contact_email': data.get('contact_email'),
            'updated_at': data.get('updated_at'),
        }

        return ordered_data

class CustomerSerializer(serializers.ModelSerializer):
    cnpj = serializers.CharField(validators=[validate_cnpj])
    phone_number = serializers.CharField(validators=[validate_phone])
    state_tax_registration = serializers.CharField(required=False, allow_blank=True, validators=[validate_state_tax_registration])

    customer_contact = CustomerContactSerializer()

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
            'customer_contact', 
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
            'customer_contact': data.get('customer_contact'),
            'created_at': data.get('created_at'),
            'updated_at': data.get('updated_at'),
        }

        return ordered_data
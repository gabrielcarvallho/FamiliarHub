from rest_framework import serializers

from apps.customers.utils import fields
from apps.customers.models import Address


class AddressSerializer(serializers.ModelSerializer):
    cep = fields.CEPField()

    class Meta:
        model = Address
        exclude = ['customer']
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_billing_address']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        ordered_data = {
            'id': representation.get('id'),
            'cep': representation.get('cep'),
            'street_name': representation.get('street_name'),
            'district': representation.get('district'),
            'number': representation.get('number'),
            'city': representation.get('city'),
            'state': representation.get('state'),
            'observation': representation.get('observation'),
            'is_billing_address': representation.get('is_billing_address')
        }

        return ordered_data
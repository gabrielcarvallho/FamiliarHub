from rest_framework import serializers

from apps.customers.utils import fields
from apps.customers.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    contact_phone = fields.PhoneNumberField()

    class Meta:
        model = Contact
        exclude = ['customer']
        read_only_fields = ['id', 'updated_at']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        ordered_data = {
            'id': representation.get('id'),
            'name': representation.get('name'),
            'date_of_birth': representation.get('date_of_birth'),
            'contact_phone': representation.get('contact_phone'),
            'contact_email': representation.get('contact_email'),
            'updated_at': representation.get('updated_at'),
        }

        return ordered_data
from rest_framework import serializers

from apps.customers.utils import fields
from apps.customers.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    contact_phone = fields.PhoneNumberField()

    class Meta:
        model = Contact
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
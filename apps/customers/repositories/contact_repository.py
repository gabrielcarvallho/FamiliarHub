from apps.customers.models import Contact


class ContactRepository:
    def create(self, contact_data: dict) -> Contact:
        Contact.objects.create(**contact_data)
    
    def save(self, obj: Contact):
        obj.save()
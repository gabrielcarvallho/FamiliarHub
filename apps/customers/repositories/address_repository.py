import uuid
from django.db.models import QuerySet
from apps.customers.models import Address


class AddressRepository:
    def exists_by_id(self, address_id: uuid.UUID) -> bool:
        return Address.objects.filter(id=address_id).exists()
    
    def get_by_id(self, address_id: uuid.UUID) -> QuerySet[Address]:
        return Address.objects.get(id=address_id)

    def create(self, address_data: dict) -> QuerySet[Address]:
        return Address.objects.create(**address_data)

    def delete(self, address_id: uuid.UUID) -> None:
        Address.objects.filter(id=address_id).delete()

    def save(slef, obj: Address) -> None:
        obj.save()
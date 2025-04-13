from rest_framework.exceptions import NotFound, ValidationError

from apps.core.services import ServiceBase
from apps.customers.repositories import AddressRepository


class AddressService(metaclass=ServiceBase):
    def __init__(self, repository=AddressRepository()):
        self.__repository = repository

    def get_address(self, address_id):
        if not self.__repository.exists_by_id(address_id):
            raise NotFound("Address not found.")
        
        return self.__repository.get_by_id(address_id)

    def update_address(self, obj, **data):
        for attr, value in data.items():
            setattr(obj, attr, value)

        self.__repository.save(obj)
        return obj
    
    def delete_address(self, address_id):
        if not self.__repository.exists_by_id(address_id):
            raise NotFound("Address not found.")
        
        address = self.__repository.get_by_id(address_id)
        if address.is_billing_address:
            raise ValidationError('Billing address cannot be deleted.')
        
        return self.__repository.delete(address_id)
from rest_framework.exceptions import NotFound, ValidationError

from apps.core.services import ServiceBase
from apps.orders.enums import DeliveryMethod
from apps.orders.repositories import StatusRepository


class StatusService(metaclass=ServiceBase):
    def __init__(self, repository=StatusRepository()):
        self.__repository = repository
    
    def get_status(self, status_id):
        if not self.__repository.exists_by_id(status_id):
            raise NotFound("Status not found.")
        
        return self.__repository.get_by_id(status_id)
    
    def get_status_by_delivery_method(self, delivery_method):
        if delivery_method not in DeliveryMethod.values:
            raise ValidationError("Invalid delivery method.")
        
        return self.__repository.get_by_delivery_method(delivery_method)

    def get_all_status(self):
        return self.__repository.get_all()
    
    def create_status(self, **data):
        self.__repository.create(data)

    def update_status(self, obj, **data):
        for attr, value in data.items():
            setattr(obj, attr, value)

        self.__repository.save(obj)
    
    def delete_status(self, status_id):
        if not self.__repository.exists_by_id(status_id):
            raise NotFound("Customer not found.")
        
        self.__repository.delete(status_id)
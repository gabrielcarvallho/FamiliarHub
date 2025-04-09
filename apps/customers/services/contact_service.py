from apps.core.services import ServiceBase
from apps.customers.repositories import ContactRepository


class ContactService(metaclass=ServiceBase):
    def __init__(self, repository=ContactRepository()):
        self.__repository = repository
    
    def create_contact(self, **data):
        return self.__repository.create(data)
    
    def update_contact(self, obj, **data):
        for attr, value in data.items():
            setattr(obj, attr, value)
        
        self.__repository.save(obj)
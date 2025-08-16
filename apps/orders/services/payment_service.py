from rest_framework.exceptions import NotFound

from apps.core.services import ServiceBase
from apps.orders.repositories import PaymentRepository


class PaymentService(metaclass=ServiceBase):
    def __init__(self, repository=PaymentRepository()):
        self.__repository = repository
    
    def get_payment_method(self, payment_id):
        if not self.__repository.exists_by_id(payment_id):
            raise NotFound('Payment method not found.')
        
        return self.__repository.get_by_id(payment_id)
    
    def get_all_payment_methods(self):
        return self.__repository.get_all()
    
    def create_payment_method(self, **data):
        self.__repository.create(data)
    
    def update_payment_method(self, obj, **data):
        for attr, value in data.items():
            setattr(obj, attr, value)

        self.__repository.save(obj)

    def delete_payment_method(self, payment_id):
        if not self.__repository.exists_by_id(payment_id):
            raise NotFound('Payment method not found.')
        
        self.__repository.delete(payment_id)
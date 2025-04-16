from apps.core.services import ServiceBase
from apps.orders.repositories import PaymentRepository


class PaymentService(metaclass=ServiceBase):
    def __init__(self, repository=PaymentRepository()):
        self.__repository = repository
    
    def get_all_payment_methods(self):
        return self.__repository.get_all()
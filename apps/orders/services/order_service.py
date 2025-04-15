from rest_framework.exceptions import NotFound, ValidationError

from apps.core.services import ServiceBase

from apps.orders.repositories.order_repository import OrderRepository
from apps.orders.repositories import StatusRepository, PaymentRepository
from apps.customers.repositories import CustomerRepository, AddressRepository


class OrderService(metaclass=ServiceBase):
    def __init__(
            self, 
            repository=OrderRepository(),
            status_repository = StatusRepository(),
            payment_repository = PaymentRepository(),
            customer_repository=CustomerRepository(),
            address_repository=AddressRepository()
        ):

        self.__repository = repository
        self.__status_repository = status_repository
        self.__payment_repository = payment_repository
        self.__customer_repository = customer_repository
        self.address_repository = address_repository

    def create_order(self, **data):
        customer_id = data.get('customer_id')
        status_id = data.get('order_status_id')
        payment_id = data.get('payment_method_id')
        delivery_address_id = data.get('delivery_address_id', None)
        new_delivery_address = data.pop('delivery_address', None)

        if not self.__customer_repository.exists_by_id(customer_id):
            raise NotFound('Customer not found.')
        
        if not self.__status_repository.exists_by_id(status_id):
            raise NotFound('Status not found.')
        
        if not self.__payment_repository.exists_by_id(payment_id):
            raise NotFound('Payment method not found.')

        if delivery_address_id:
            if not self.address_repository.exists_by_id(delivery_address_id):
                raise NotFound('Delivery address not found.')
            
            address = self.address_repository.get_by_id(delivery_address_id)
            if address.customer.id != customer_id:
                raise ValidationError('Delivery address provided does not belong to the customer.')
        else:
            new_delivery_address['customer_id'] = customer_id
            address = self.address_repository.create(new_delivery_address)

            data['delivery_address_id'] = address.id

        for key, value in data.items():
            print({key: value})
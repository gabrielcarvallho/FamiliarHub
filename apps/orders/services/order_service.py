from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError

from apps.core.services import ServiceBase
from apps.logistics.services import ProductionScheduleService

from apps.orders.repositories import ProductOrderRepository
from apps.logistics.repositories import ProductionScheduleRepository
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
            address_repository=AddressRepository(),
            product_order_repository = ProductOrderRepository(),
            production_repository=ProductionScheduleRepository(),

            production_service = ProductionScheduleService()
        ):

        self.__repository = repository
        self.__status_repository = status_repository
        self.__payment_repository = payment_repository
        self.__customer_repository = customer_repository
        self.__address_repository = address_repository
        self.__production_repository = production_repository
        self.__product_order_repository = product_order_repository

        self.__production_service = production_service

    def get_order(self, order_id):
        if not self.__repository.exists_by_id(order_id):
            raise NotFound('Order not found.')
        
        return self.__repository.get_by_id(order_id)
    
    def get_orders_by_user(self, user):
        if not user.groups.filter(name='delivery_person'):
            return self.__repository.filter(
                created_by_id=user.id
            )
        else:
            return self.__repository.filter(
                order_status__identifier=2
            )
    
    def get_all_orders(self):
        return self.__repository.get_all()

    @transaction.atomic
    def create_order(self, request, **data):
        customer_id = data.get('customer_id')
        status_id = data.get('order_status_id')
        payment_id = data.get('payment_method_id')
        delivery_address_id = data.get('delivery_address_id', None)
        new_delivery_address = data.pop('delivery_address', None)
        delivery_date = data['delivery_date']
        products = data.pop('products')

        if not self.__customer_repository.exists_by_id(customer_id):
            raise NotFound('Customer not found.')
        
        if not self.__status_repository.exists_by_id(status_id):
            raise NotFound('Status not found.')
        
        if not self.__payment_repository.exists_by_id(payment_id):
            raise NotFound('Payment method not found.')

        if delivery_address_id:
            if not self.__address_repository.exists_by_id(delivery_address_id):
                raise NotFound('Delivery address not found.')
            
            address = self.__address_repository.get_by_id(delivery_address_id)
            if address.customer.id != customer_id:
                raise ValidationError('Delivery address provided does not belong to the customer.')
        else:
            new_delivery_address['customer_id'] = customer_id
            address = self.__address_repository.create(new_delivery_address)

            data['delivery_address_id'] = address.id
        
        data['created_by_id'] = request.user.id

        production_schedule = self.__production_service.validate_production(products, delivery_date)

        order = self.__repository.create(data)
        for product in products:
            product['order_id'] = order.id
        
        for production in production_schedule:
            production['order_id'] = order.id
        
        self.__product_order_repository.bulk_create(products)
        self.__production_repository.bulk_create(production_schedule)
    
    def delete_order(self, order_id):
        if not self.__repository.exists_by_id(order_id):
            raise NotFound('Order not found.')

        self.__repository.delete(order_id)
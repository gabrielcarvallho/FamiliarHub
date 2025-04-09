from django.db import transaction

from rest_framework.exceptions import ValidationError, NotFound

from apps.core.services import ServiceBase
from apps.customers.services import ContactService
from apps.customers.repositories import CustomerRepository


class CustomerService(metaclass=ServiceBase):
    def __init__(
            self, 
            repository=CustomerRepository(),
            contact_service=ContactService()
        ):

        self.__repository = repository
        self.__contact_service = contact_service

    def get_customer(self, customer_id):
        if not self.__repository.exists_by_id(customer_id):
            raise NotFound('Customer not found.')
        
        return self.__repository.get_by_id(customer_id)
    
    def get_all_customers(self):
        customers = self.__repository.get_all()

        if not customers:
            raise NotFound('No customers found.')
        
        return customers

    @transaction.atomic
    def create_customer(self, **data):
        cnpj = data.get('cnpj')
        contact = data.pop('contact')

        if self.__repository.exists_by_cnpj(cnpj):
            raise ValidationError('This CNPJ is already in use.')

        customer = self.__repository.create(data)

        contact['customer_id'] = customer.id
        self.__contact_service.create_contact(**contact)

        return customer
    
    @transaction.atomic
    def update_customer(self, obj, **data):
        contact = data.pop('contact', None)

        for attr, value in data.items():
            setattr(obj, attr, value)

        self.__repository.save(obj)

        if contact:
            self.__contact_service.update_contact(obj.contact, **contact)
            
        return obj
    
    def delete_customer(self, customer_id):
        if not self.__repository.exists_by_id(customer_id):
            raise NotFound("Customer not found.")
        
        self.__repository.delete(customer_id)
from django.db import transaction
from rest_framework.exceptions import ValidationError, NotFound

from apps.core.services import ServiceBase
from apps.customers.repositories import (
    CustomerRepository, 
    AddressRepository, 
    ContactRepository
)


class CustomerService(metaclass=ServiceBase):
    def __init__(
            self, 
            repository=CustomerRepository(),
            address_repository=AddressRepository(),
            contact_repository=ContactRepository()
        ):

        self.__repository = repository
        self.__address_repository = address_repository
        self.__contact_repository = contact_repository

    def get_customer(self, customer_id):
        if not self.__repository.exists_by_id(customer_id):
            raise NotFound('Customer not found.')
        
        return self.__repository.get_by_id(customer_id)
    
    def get_to_update(self, customer_id):
        if not self.__repository.exists_by_id(customer_id):
            raise NotFound('Customer not found.')
        
        return self.__repository.filter_by_address(customer_id)

    def get_all_customers(self):
        return self.__repository.get_all()

    @transaction.atomic
    def create_customer(self, request, **data):
        cnpj = data.get('cnpj')
        contact_data = data.pop('contact')
        address_data = data.pop('billing_address')

        if self.__repository.exists_by_cnpj(cnpj):
            raise ValidationError('This CNPJ is already in use.')
        
        data['created_by_id'] = request.user.id
        customer = self.__repository.create(data)

        contact_data['customer_id'] = customer.id
        address_data['customer_id'] = customer.id
        address_data['is_billing_address'] = True

        self.__address_repository.create(address_data)
        self.__contact_repository.create(contact_data)

        return customer
    
    @transaction.atomic
    def update_customer(self, obj, **data):
        address_data = data.pop('billing_address', None)
        contact_data = data.pop('contact', None)

        for attr, value in data.items():
            setattr(obj, attr, value)
        
        if address_data:
            for attr, value in address_data.items():
                setattr(obj.billing_address[0], attr, value)
            
            self.__address_repository.save(obj.billing_address[0])

        if contact_data:
            for attr, value in contact_data.items():
                setattr(obj.contact, attr, value)

            self.__contact_repository.save(obj.contact)

        self.__repository.save(obj)
        return obj
    
    def delete_customer(self, customer_id):
        if not self.__repository.exists_by_id(customer_id):
            raise NotFound("Customer not found.")
        
        self.__repository.delete(customer_id)
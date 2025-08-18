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
        document = data.get('document')
        contact_data = data.pop('contact', None)
        address_data = data.pop('billing_address')

        if self.__repository.exists_by_document(document):
            raise ValidationError('This document is already in use.')
        
        data['created_by_id'] = request.user.id
        customer = self.__repository.create(data)

        address_data['customer_id'] = customer.id
        address_data['is_billing_address'] = True

        self.__address_repository.create(address_data)
            
        if contact_data:
            contact_data['customer_id'] = customer.id
            self.__contact_repository.create(contact_data)
    
    @transaction.atomic
    def update_customer(self, obj, **data):
        document = data.get('document')
        address_data = data.pop('billing_address', None)
        contact_data = data.pop('contact', None)

        for attr, value in data.items():
            setattr(obj, attr, value)
        
        for attr, value in address_data.items():
            setattr(obj.billing_address[0], attr, value)

        if contact_data:
            if hasattr(obj, 'contact') and obj.contact:
                for attr, value in contact_data.items():
                    setattr(obj.contact, attr, value)
                self.__contact_repository.save(obj.contact)
            else:
                contact_data['customer_id'] = obj.id

                new_contact = self.__contact_repository.create(contact_data)
                obj.contact = new_contact

        self.__repository.save(obj)
        self.__address_repository.save(obj.billing_address[0])
    
    def delete_customer(self, customer_id):
        if not self.__repository.exists_by_id(customer_id):
            raise NotFound("Customer not found.")
        
        self.__repository.delete(customer_id)
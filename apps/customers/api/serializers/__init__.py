from .contact_serializer import ContactSerializer
from .address_serializer import AddressSerializer
from .customer_serializer import CustomerSerializer, CreateCustomerSerializer, UpdateCustomerSerializer


__all__ = [
    'CustomerSerializer',
    'CreateCustomerSerializer',
    'UpdateCustomerSerializer',
    'CustomerCustomSerializer',
    'ContactSerializer',
    'AddressSerializer'
]
from .contact_serializer import ContactSerializer
from .address_serializer import AddressSerializer
from .customer_serializer import CustomerSerializer, CustomerCustomSerializer


__all__ = [
    'CustomerSerializer',
    'CustomerCustomSerializer',
    'ContactSerializer',
    'AddressSerializer'
]
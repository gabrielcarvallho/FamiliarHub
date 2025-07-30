import uuid
from django.db import models

from apps.accounts.models import CustomUser
from apps.customers.enums import CustomerType


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_type = models.CharField(max_length=2, choices=CustomerType.choices) # PF, PJ
    document = models.CharField(max_length=14, unique=True) # CPF, CNPJ
    name = models.CharField(max_length=100)
    fantasy_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    state_registration = models.CharField(max_length=20, null=True, blank=True)

    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='owner_customers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='contact')
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()

    updated_at = models.DateTimeField(auto_now=True)

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    cep = models.CharField(max_length=8)
    street_name = models.CharField(max_length=90)
    district = models.CharField(max_length=50)
    number = models.CharField(max_length=5)
    city = models.CharField(max_length=70)
    state = models.CharField(max_length=2)
    observation = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=70, null=True, blank=True)
    is_billing_address = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
import uuid
from django.db import models


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    state_tax_registration = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CustomerContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='customer_contact')
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()

    updated_at = models.DateTimeField(auto_now=True)
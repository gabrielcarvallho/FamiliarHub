import uuid
from datetime import timedelta

from django.db import models

from apps.products.models import Product
from apps.accounts.models import CustomUser
from apps.customers.models import Customer, Address


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    is_requires_due_date = models.BooleanField(default=False)
    additional_info = models.JSONField(null=True, blank=True)

class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=120)
    identifier = models.IntegerField()

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    payment_method = models.ForeignKey(Payment, on_delete=models.PROTECT)
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    delivery_date = models.DateField()

    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='owner_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.product_items.all())
    
    @property
    def payment_due_date(self):
        additional_info = self.payment_method.additional_info or {}
        due_days = additional_info.get('due_days', 0)
        
        return self.delivery_date + timedelta(days=due_days)

class ProductOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='product_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return self.quantity * self.product.price
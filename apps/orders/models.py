import uuid
from datetime import timedelta

from django.db import models, transaction
from apps.orders.utils.date_utils import DateUtils

from apps.products.models import Product
from apps.accounts.models import CustomUser
from apps.customers.models import Customer, Address
from apps.orders.enums import StatusCategory, DeliveryMethod


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    is_requires_due_date = models.BooleanField(default=False)
    additional_info = models.JSONField(null=True, blank=True)

class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=120)
    category = models.IntegerField(choices=StatusCategory)
    delivery_method = models.CharField(max_length=8, choices=DeliveryMethod, null=True, blank=True)
    sequence_order = models.IntegerField()

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.IntegerField(unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    payment_method = models.ForeignKey(Payment, on_delete=models.PROTECT)
    payment_due_days = models.PositiveIntegerField(null=True, blank=True)

    delivery_method = models.CharField(max_length=8, choices=DeliveryMethod)
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_date = models.DateField()

    order_status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    is_delivered = models.BooleanField(default=False)

    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='owner_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    table_order = models.IntegerField(null=True, blank=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.product_items.all())
    
    @property
    def payment_due_date(self):
        if not self.payment_method.is_requires_due_date:
            return None
        
        due_days = self.payment_due_days
        if not due_days:
            additional_info = self.payment_method.additional_info or {}
            due_days = additional_info.get('due_days', 0)
        
        due_date = self.delivery_date + timedelta(days=due_days)
        return DateUtils.get_next_business_day(due_date)
    
    def save(self, *args, **kwargs):
        if self.order_number is None:
            with transaction.atomic():
                last_order = Order.objects.order_by('-order_number').first()
                self.order_number = 1 if not last_order else last_order.order_number + 1
        
        if self.payment_method.is_requires_due_date and not self.payment_due_days:
            additional_info = self.payment_method.additional_info
            self.payment_due_days = additional_info.get('due_days')

        super().save(*args, **kwargs)

class ProductOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='product_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'product'], name='unique_product_per_order')
        ]

    @property
    def total_price(self):
        return self.quantity * self.sale_price
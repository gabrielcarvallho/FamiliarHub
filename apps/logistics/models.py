import uuid
from django.db import models
from apps.orders.models import Order
from apps.products.models import Product


class ProductionSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='production_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="production_schedule")
    production_date = models.DateField()
    batches = models.PositiveIntegerField()

    class Meta:
        unique_together = ('product', 'order', 'production_date')
        ordering = ['production_date']
import uuid
from django.db import models

from apps.products.models import Product


class StockConfiguration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock_settings')
    current_stock = models.IntegerField(default=0)

    min_stock_threshold = models.IntegerField(default=0)
    max_stock_capacity = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
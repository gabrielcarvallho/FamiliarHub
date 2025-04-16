import uuid
from django.db import models
from apps.products.models import Product


class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_inventory")
    date = models.DateField()
    quantity = models.IntegerField(default=0)
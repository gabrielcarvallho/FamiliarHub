import uuid
from django.db import models

from apps.products.models import Product
from apps.accounts.models import CustomUser

from apps.production.enums import ProductionStatus


class ProductionRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.IntegerField(choices=ProductionStatus)
    notes = models.CharField(max_length=900, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def duration_days(self):
        if self.end_date:
            return (self.end_date - self.start_date).days
        
        return None

class ProductionItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    production_record = models.ForeignKey(ProductionRecord, on_delete=models.CASCADE, related_name='production_items')
    quantity_produced = models.IntegerField()
    expiration_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
import uuid
from datetime import date
from django.db.models import QuerySet
from apps.logistics.models import Inventory


class InventoryRepository:
    def filter(self, product_ids: list[uuid.UUID], reference_date: date) -> QuerySet[Inventory]:
        return Inventory.objects.filter(
            product_id__in=product_ids,
            date__lte=reference_date
        ).order_by('product_id', '-date')
    
    def bulk_update(self, inventory_data: list[Inventory]):
        if inventory_data:
            Inventory.objects.bulk_update(inventory_data, ['quantity'])
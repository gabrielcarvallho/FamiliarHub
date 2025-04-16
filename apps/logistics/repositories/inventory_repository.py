import uuid
from django.db.models import QuerySet
from apps.logistics.models import Inventory


class InventoryRepository:
    def get(self, product_id: uuid.UUID, date) -> QuerySet[Inventory]:
        return Inventory.objects.filter(
            product_id=product_id,
            date__lte=date
        )
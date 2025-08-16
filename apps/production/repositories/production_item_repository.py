import uuid
from typing import List
from django.db.models import QuerySet
from apps.production.models import ProductionItem


class ProductionItemRepository:
    def filter_by_production_record_id(self, production_record_id: uuid.UUID) -> QuerySet[ProductionItem]:
        return ProductionItem.objects.filter(production_record_id=production_record_id)
    
    def bulk_create(self, items_data: List[ProductionItem]) -> None:
        ProductionItem.objects.bulk_create(items_data)
    
    def delete(self, production_record_id: uuid.UUID) -> None:
        ProductionItem.objects.filter(production_record_id=production_record_id).delete()
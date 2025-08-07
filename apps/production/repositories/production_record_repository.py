import uuid
from django.db.models import QuerySet
from apps.production.models import ProductionRecord


class ProductionRecordRepository:
    def exists_by_id(self, record_id: uuid.UUID) -> bool:
        return ProductionRecord.objects.filter(id=record_id).exists()
    
    def get_by_id(self, record_id: uuid.UUID) -> QuerySet[ProductionRecord]:
        return ProductionRecord.objects.select_related('created_by').prefetch_related(
            'production_items__product'
        ).get(id=record_id)

    def get_all(self, start_date=None, end_date=None) -> QuerySet[ProductionRecord]:
        queryset = ProductionRecord.objects.select_related('created_by').prefetch_related('production_items__product')

        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(start_date__lte=end_date)
            
        return queryset.order_by('-start_date', '-created_at')
    
    def create(self, product_data: dict) -> QuerySet[ProductionRecord]:
        return ProductionRecord.objects.create(**product_data)
    
    def save(self, obj: ProductionRecord) -> None:
        obj.save()
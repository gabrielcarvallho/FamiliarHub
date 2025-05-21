import uuid
from datetime import date
from django.db.models import QuerySet

from apps.logistics.models import ProductionSchedule


class ProductionScheduleRepository:
    def filter(self, product_ids: list[uuid.UUID], reference_date: date) -> QuerySet[ProductionSchedule]:
        return ProductionSchedule.objects.filter(
            product_id__in=product_ids,
            production_date__gte = reference_date
        ).order_by('production_date')
    
    def filter_by_date(self, date: date) -> QuerySet[ProductionSchedule]:
        return ProductionSchedule.objects.filter(production_date=date).select_related('product')
    
    def create_or_update(self, production_schedule: list) -> None:
        for alloc in production_schedule:
            obj, created = ProductionSchedule.objects.get_or_create(
                product_id=alloc['product_id'],
                production_date=alloc['production_date'],
                defaults={
                    'batches': alloc['batches'],
                    'packages': alloc['packages'],
                }
            )
            if not created and (obj.batches != alloc['batches'] or obj.packages != alloc['packages']):
                obj.batches = alloc['batches']
                obj.packages = alloc['packages']
                obj.save()
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
    
    def filter_excluding_orders(self, product_ids, reference_date, exclude_order_ids):
        return ProductionSchedule.objects.filter(
            product_id__in=product_ids,
            production_date__gte=reference_date
        ).exclude(
            order_id__in=exclude_order_ids
        ).order_by('production_date')
    
    def create_or_update(self, production_schedule: list) -> None:
        for alloc in production_schedule:
            obj, created = ProductionSchedule.objects.get_or_create(
                product_id=alloc['product_id'],
                order_id=alloc['order_id'],
                production_date=alloc['production_date'],
                defaults={
                    'batches': alloc['batches'],
                    'packages': alloc['packages'],
                }
            )
            if not created:
                obj.batches += alloc['batches']
                obj.packages += alloc['packages']
                obj.save()
    
    def delete_by_order_id(self, order_id: uuid.UUID) -> None:
        ProductionSchedule.objects.filter(order_id=order_id).delete()
    
    def delete_by_order_ids(self, order_ids: uuid.UUID) -> None:
        ProductionSchedule.objects.filter(order_id__in=order_ids).delete()
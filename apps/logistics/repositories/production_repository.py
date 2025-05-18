import uuid
from datetime import date
from django.db.models import Sum
from django.db.models import QuerySet

from apps.logistics.models import ProductionSchedule


class ProductionScheduleRepository:
    def filter(self, product_ids: list[uuid.UUID], reference_date: date) -> QuerySet[ProductionSchedule]:
        return ProductionSchedule.objects.filter(
            product_id__in=product_ids,
            production_date__gte = reference_date
        ).order_by('production_date')
    
    def get_batches_by_date(self, date: date) -> QuerySet[ProductionSchedule]:
        return ProductionSchedule.objects.filter(
            production_date=date
        ).values('product__id', 'product__name').annotate(total_batches=Sum('batches'))
    
    def get_orders_by_date(self, date: date) -> QuerySet[ProductionSchedule]:
        return ProductionSchedule.objects.filter(
            production_date=date
        ).values_list('order_id', flat=True)
    
    def bulk_create(self, production_data: list) -> None:
        model_instances = [ProductionSchedule(
            order_id=item['order_id'],
            product_id=item['product_id'],
            production_date=item['production_date'],
            batches=item['batches']
        ) for item in production_data]

        ProductionSchedule.objects.bulk_create(objs=model_instances)
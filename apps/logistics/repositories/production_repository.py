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
    
    def bulk_create(self, production_data: list) -> None:
        model_instances = [ProductionSchedule(
            order_id=item['order_id'],
            product_id=item['product_id'],
            production_date=item['production_date'],
            batches=item['batches']
        ) for item in production_data]

        ProductionSchedule.objects.bulk_create(objs=model_instances)
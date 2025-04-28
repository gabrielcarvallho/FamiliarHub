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
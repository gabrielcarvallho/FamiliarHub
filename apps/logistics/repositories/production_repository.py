import uuid
from apps.logistics.models import ProductionSchedule


class ProductionScheduleRepository:
    def count(self, product_id: uuid.UUID, date):
        return ProductionSchedule.objects.filter(
            product_id=product_id,
            date=date
        )
import uuid
from django.db.models import QuerySet
from apps.orders.models import Status


class StatusRepository:
    def exists_by_id(self, status_id: uuid.UUID) -> bool:
        return Status.objects.filter(id=status_id).exists()
    
    def get_all(self) -> QuerySet[Status]:
        return Status.objects.all()
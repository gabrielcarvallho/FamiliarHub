import uuid
from django.db.models import Q, QuerySet

from apps.orders.models import Status


class StatusRepository:
    def exists_by_id(self, status_id: uuid.UUID) -> bool:
        return Status.objects.filter(id=status_id).exists()
    
    def get_by_id(self, status_id: uuid.UUID) -> QuerySet[Status]:
        return Status.objects.get(id=status_id)
    
    def get_by_sequence_order(self, sequence_order: int) -> QuerySet[Status]:
        return Status.objects.get(sequence_order=sequence_order)
    
    def get_by_delivery_method(self, delivery_method: str):
        return Status.objects.filter(
            Q(delivery_method=None) | Q(delivery_method=delivery_method)
        ).order_by('sequence_order')
    
    def get_all(self) -> QuerySet[Status]:
        return Status.objects.all().order_by('sequence_order')
    
    def create(self, status_data: dict) -> None:
        Status.objects.create(**status_data)

    def delete(self, status_id: uuid.UUID) -> None:
        Status.objects.filter(id=status_id).delete()

    def save(self, obj: Status) -> None:
        obj.save()
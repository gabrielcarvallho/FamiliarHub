import uuid
from django.db.models import QuerySet

from apps.orders.models import Order


class OrderRepository:
    def exists_by_id(self, order_id: uuid.UUID) -> bool:
        return Order.objects.filter(id=order_id).exists()
    
    def get_by_id(self, order_id: uuid.UUID) -> QuerySet[Order]:
        return Order.objects.get(id=order_id)
    
    def create(self, order_data: dict) -> QuerySet[Order]:
        return Order.objects.create(**order_data)
    
    def delete(self, order_id: uuid.UUID) -> None:
        Order.objects.filter(id=order_id).delete()

    def save(self, obj: Order) -> None:
        obj.save()
import uuid
from django.db.models import QuerySet

from apps.orders.models import Order


class OrderRepository:
    def exists_by_id(self, order_id: uuid.UUID) -> bool:
        return Order.objects.filter(id=order_id).exists()
    
    def get_by_id(self, order_id: uuid.UUID) -> QuerySet[Order]:
        return Order.objects.prefetch_related('product_items').get(id=order_id)
    
    def get_all(self) -> list[QuerySet[Order]]:
        return Order.objects.all()
    
    def filter(self, **params):
        return Order.objects.prefetch_related('product_items').filter(**params)
    
    def create(self, order_data: dict) -> QuerySet[Order]:
        return Order.objects.create(**order_data)
    
    def delete(self, order_id: uuid.UUID) -> None:
        Order.objects.filter(id=order_id).delete()
    
    def update(self, obj: QuerySet[Order], **params) -> None:
        obj.update(**params)

    def save(self, obj: Order) -> None:
        obj.save()
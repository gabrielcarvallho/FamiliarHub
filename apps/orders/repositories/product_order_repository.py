from django.db.models import QuerySet
from apps.orders.models import ProductOrder


class ProductOrderRepository:
    def create(self, product_order_data: dict) -> QuerySet[ProductOrder]:
        return ProductOrder.objects.create(**product_order_data)
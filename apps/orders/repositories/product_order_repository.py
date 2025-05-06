import uuid
from django.db.models import Sum
from django.db.models import QuerySet
from apps.orders.models import ProductOrder


class ProductOrderRepository:
    def filter_by_orders(self, order_ids: uuid.UUID) -> QuerySet[ProductOrder]:
        return ProductOrder.objects.filter(
            order_id__in=order_ids
        ).values('product__id', 'product__name').annotate(total_packages=Sum('quantity'))

    def bulk_create(self, product_order_data: list) -> None:
        model_instances = [ProductOrder(
            order_id=item['order_id'],
            product_id=item['product_id'],
            quantity=item['quantity']
        ) for item in product_order_data]
        
        ProductOrder.objects.bulk_create(objs=model_instances)
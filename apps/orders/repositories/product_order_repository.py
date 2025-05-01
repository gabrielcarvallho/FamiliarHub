from django.db.models import QuerySet
from apps.orders.models import ProductOrder


class ProductOrderRepository:
    def bulk_create(self, product_order_data: list) -> None:
        model_instances = [ProductOrder(
            order_id=item['order_id'],
            product_id=item['product_id'],
            quantity=item['quantity']
        ) for item in product_order_data]
        
        ProductOrder.objects.bulk_create(objs=model_instances)
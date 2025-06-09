import uuid
from datetime import date
from django.db.models import Sum
from django.db.models import QuerySet
from apps.orders.models import ProductOrder


class ProductOrderRepository:
    def get_orders_by_product_and_date(self, product_ids, start_date: date, end_date: date) -> QuerySet[ProductOrder]:
        return (
            ProductOrder.objects.filter(
                product_id__in=product_ids,
                order__delivery_date__gte=start_date,
                order__delivery_date__lte=end_date
            )
            .values('product_id', 'order__delivery_date')
            .annotate(total_packages=Sum('quantity'))
            .order_by('product_id', 'order__delivery_date')
        )

    def filter_by_order_id(self, order_id: uuid.UUID):
        return ProductOrder.objects.filter(order_id=order_id)
    
    def filter_by_orders(self, order_ids: uuid.UUID) -> QuerySet[ProductOrder]:
        return ProductOrder.objects.filter(
            order_id__in=order_ids
        ).values('product__id', 'product__name').annotate(total_packages=Sum('quantity'))

    def bulk_create(self, product_order_data: list) -> None:
        model_instances = [ProductOrder(
            order_id=item['order_id'],
            product_id=item['product_id'],
            quantity=item['quantity'],
            sale_price=item['sale_price']
        ) for item in product_order_data]
        
        ProductOrder.objects.bulk_create(objs=model_instances)
    
    def bulk_update(self, instances, fields):
        ProductOrder.objects.bulk_update(instances, fields)
    
    def delete(self, order_id: uuid.UUID, product_ids: uuid.UUID) -> None:
        ProductOrder.objects.filter(
            order_id=order_id,
            product_id__in=product_ids
        ).delete()
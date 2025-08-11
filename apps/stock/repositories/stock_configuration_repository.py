import uuid
from django.db.models import QuerySet

from apps.stock.models import StockConfiguration


class StockConfigurationRepository:
    def exists_by_id(self, configuration_id: uuid.UUID) -> bool:
        return StockConfiguration.objects.filter(id=configuration_id).exists()
    
    def get_by_id(self, configuration_id: uuid.UUID) -> QuerySet[StockConfiguration]:
        return StockConfiguration.objects.select_related('product').get(
            id=configuration_id
        )
    
    def get_all(self) -> QuerySet[StockConfiguration]:
        return StockConfiguration.objects.select_related('product').filter(
            is_active=True
        ).order_by('product__name')
    
    def exists_by_product_id(self, product_id: uuid.UUID) -> bool:
        return StockConfiguration.objects.filter(product_id=product_id).exists()
    
    def create(self, configuration_data: dict) -> None:
        StockConfiguration.objects.create(**configuration_data)

    def soft_delete(self, product_id: uuid.UUID) ->  None:
        StockConfiguration.objects.filter(product_id=product_id).update(is_active=False, current_stock=0)

    def save(self, obj: StockConfiguration) -> None:
        obj.save()
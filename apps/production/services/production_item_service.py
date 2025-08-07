import uuid
from django.utils import timezone
from django.db import transaction
from rest_framework.exceptions import NotFound, ValidationError

from apps.core.services import ServiceBase
from apps.production.models import ProductionItem
from apps.products.repositories import ProductRepository
from apps.production.repositories import ProductionItemRepository


class ProductionItemService(metaclass=ServiceBase):
    def __init__(
            self, 
            repository=ProductionItemRepository(),
            product_repository=ProductRepository()
        ):

        self.__repository = repository
        self.__product_repository = product_repository

    @transaction.atomic
    def create_items(self, production_record, items_data):
        production_items = []
        today = timezone.now().date()

        product_ids = list(set([uuid.UUID(str(item['product_id'])) for item in items_data]))
        products = {p.id: p for p in self.__product_repository.filter_by_id(product_ids)}

        if len(products) != len(set(product_ids)):
            missing_ids = set(product_ids) - set(products.keys())
            raise ValidationError(f"Products not found: {', '.join(str(pid) for pid in missing_ids)}")
        
        for item_data in items_data:
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity_produced')
            expiration_date = item_data.get('expiration_date')

            if quantity <= 0:
                raise ValidationError(f"Quantity must be greater than zero for product {product_id}")

            if expiration_date and expiration_date <= today:
                raise ValidationError(f"Expiration date must be greater than current date for product {product_id}")
            
            production_items.append(ProductionItem(
                production_record_id=production_record.id,
                product_id=product_id,
                quantity_produced=quantity,
                expiration_date=expiration_date
            ))
        
        self.__repository.bulk_create(production_items)
    
    @transaction.atomic
    def update_production_items(self, production_record, items_data):
        self.__repository.delete(production_record.id)
        self.create_items(production_record, items_data)
    
    @transaction.atomic
    def update_current_stock(self, production_record):
        items = self.__repository.filter_by_production_record_id(production_record.id)

        for item in items:
            product = item.product
            product.current_stock += item.quantity_produced

            self.__product_repository.save(product)
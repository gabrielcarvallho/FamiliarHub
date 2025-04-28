from django.db import transaction
from django.utils import timezone
from collections import defaultdict
from rest_framework.exceptions import ValidationError

from apps.core.services import ServiceBase
from apps.products.repositories import ProductRepository
from apps.logistics.repositories import InventoryRepository


class InventoryService(metaclass=ServiceBase):
    def __init__(
            self,
            product_repository=ProductRepository(),
            inventory_repository=InventoryRepository()
        ):
        
        self.__product_repository = product_repository
        self.__repository = inventory_repository
    
    @transaction.atomic
    def process_inventory(self, products_data):
        entries_to_update = []
        consumed_map = defaultdict(int)
        remaining_map = defaultdict(int)

        consumption_date = timezone.now().date()
        product_ids = [item['product_id'] for item in products_data]

        existing_ids = set(self.__product_repository.get_existing_ids(product_ids))
        missing_products = [str(pid) for pid in product_ids if pid not in existing_ids]

        if missing_products:
            raise ValidationError(f"Products not found. {', '.join(missing_products)}")
        
        inventory_entries = self.__repository.filter(
            product_ids=product_ids,
            reference_date=consumption_date
        )

        latest_entry_map = {}
        for entry in inventory_entries:
            if entry.product_id not in latest_entry_map:
                latest_entry_map[entry.product_id] = entry
        
        for product in products_data:
            product_id = product['product_id']
            required = product['quantity']

            latest_entry = latest_entry_map.get(product_id)
            stock_available = latest_entry.quantity if latest_entry else 0

            quantity_consumed = min(required, stock_available)

            if latest_entry and quantity_consumed > 0:
                latest_entry.quantity -= quantity_consumed
                entries_to_update.append(latest_entry)
            
            consumed_map[product_id] = quantity_consumed
            remaining_map[product_id] = required - quantity_consumed
        
        if entries_to_update:
            self.__repository.bulk_update(entries_to_update)
        
        return consumed_map, remaining_map
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
        self.__inventory_repository = inventory_repository
    
    def consume_inventory(self, products_data, delivery_date):
        updates = []
        consumed_map = {}
        remaining_map = {}
        inventory_map = defaultdict(list)

        product_ids = [item['product_id'] for item in products_data]
        existing_ids = set(self.__product_repository.get_existing_ids(product_ids))

        missing_products = [str(pid) for pid in product_ids if pid not in existing_ids]
        if missing_products:
            raise ValidationError(f"Products not found. {', '.join(missing_products)}")
        
        inventory_entries = self.__inventory_repository.filter_by_id(
            product_ids, delivery_date
        )

        for entry in inventory_entries:
            inventory_map[entry.product_id].append(entry)

        for item in products_data:
            product_id = item['product_id']
            required = item['quantity']
            entries = inventory_map.get(product_id, [])

            total_consumed = 0
            for entry in entries:
                if total_consumed >= required:
                    break

                available = entry.quantity
                to_consume = min(available, required - total_consumed)

                entry.quantity -= to_consume
                total_consumed += to_consume

                if to_consume > 0:
                    updates.append(entry)

            consumed_map[product_id] = total_consumed
            remaining_map[product_id] = required - total_consumed
        
        if updates:
            self.__inventory_repository.bulk_update(updates)

        return consumed_map, remaining_map
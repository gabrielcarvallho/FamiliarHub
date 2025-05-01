import math
from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.core.services import ServiceBase
from apps.products.repositories import ProductRepository
from apps.logistics.repositories import ProductionScheduleRepository


class ProductionScheduleService(metaclass=ServiceBase):
    def __init__(
            self, 
            repository=ProductionScheduleRepository(),
            product_repository=ProductRepository()
        ):
        self.__repository = repository
        self.__product_repository = product_repository
    
    def validate_production(self, products_data, delivery_date):
        start_date = timezone.now().date() + timedelta(days=1)
        product_ids = [item['product_id'] for item in products_data]

        existing_ids = set(self.__product_repository.get_existing_ids(product_ids))
        missing_products = [str(pid) for pid in product_ids if pid not in existing_ids]

        if missing_products:
            raise ValidationError(f"Products not found. {', '.join(missing_products)}")

        products = self.__product_repository.filter_by_id(product_ids)
        schedules = self.__repository.filter(
            product_ids=product_ids,
            reference_date=start_date
        )

        production_map = {}
        for item in schedules:
            production_map.setdefault(item.product_id, {})[item.production_date] = item.batches

        allocations = []

        for item in products_data:
            product_id = item['product_id']
            total_packages = item['quantity']

            product = products.get(id=product_id)

            batches_required = math.ceil(total_packages / product.batch_packages)
            daily_capacity = math.floor(product.daily_batch_capacity * 0.8)

            current_date = start_date
            allocated_batches = 0

            while current_date <= delivery_date and allocated_batches < batches_required:
                if current_date.weekday() >= 5:
                    current_date += timedelta(days=1)
                    continue

                used_capacity = production_map.get(product_id, {}).get(current_date, 0)
                available_capacity = daily_capacity - used_capacity

                if available_capacity <= 0:
                    current_date += timedelta(days=1)
                    continue

                batches_today = min(available_capacity, batches_required - allocated_batches)

                can_fit_batch = True
                for offset in range(product.batch_production_days):
                    check_date = current_date + timedelta(days=offset)
                    if check_date.weekday() >= 5 or check_date > delivery_date:
                        can_fit_batch = False
                        break

                    used = production_map.get(product_id, {}).get(check_date, 0)
                    if used >= daily_capacity:
                        can_fit_batch = False
                        break

                if can_fit_batch:
                    for offset in range(product.batch_production_days):
                        prod_date = current_date + timedelta(days=offset)
                        production_map.setdefault(product_id, {})
                        production_map[product_id][prod_date] = production_map[product_id].get(prod_date, 0) + batches_today

                        allocations.append({
                            "product_id": product_id,
                            "production_date": prod_date,
                            "batches": batches_today
                        })

                    allocated_batches += batches_today
                else:
                    current_date += timedelta(days=1)

            if allocated_batches < batches_required:
                raise ValidationError(f"Unable to allocate production for product {product.name} by delivery date.")

        return allocations
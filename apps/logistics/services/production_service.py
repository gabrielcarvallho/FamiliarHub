import uuid
import math
from datetime import timedelta
from collections import defaultdict

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.core.services import ServiceBase
from apps.products.repositories import ProductRepository
from apps.orders.repositories import ProductOrderRepository
from apps.logistics.repositories import ProductionScheduleRepository


class ProductionScheduleService(metaclass=ServiceBase):
    def __init__(
            self, 
            repository=ProductionScheduleRepository(),
            product_repository=ProductRepository(),
            product_order_repository=ProductOrderRepository()
        ):

        self.__repository = repository
        self.__product_repository = product_repository
        self.__product_order_repository = product_order_repository
    
    def validate_production(self, products_data, delivery_date):
        start_date = timezone.now().date() + timedelta(days=1)
        product_ids = [uuid.UUID(str(item['product_id'])) for item in products_data]

        existing_ids = set(self.__product_repository.get_existing_ids(product_ids))
        missing_products = [str(pid) for pid in product_ids if pid not in existing_ids]

        if missing_products:
            raise ValidationError(f"Products not found. {', '.join(missing_products)}")

        products = {p.id: p for p in self.__product_repository.filter_by_id(product_ids)}

        schedules = self.__repository.filter(
            product_ids=product_ids,
            reference_date=start_date
        )

        production_map = defaultdict(lambda: defaultdict(int))
        for item in schedules:
            production_map[item.product_id][item.production_date] += item.batches

        ordered_packages_map = defaultdict(lambda: defaultdict(int))
        
        orders = self.__product_order_repository.get_orders_by_product_and_date(product_ids, start_date, delivery_date)
        for order in orders:
            ordered_packages_map[order['product_id']][order['order__delivery_date']] += order['total_packages']

        for item in products_data:
            product_id = uuid.UUID(str(item['product_id']))
            quantity = item['quantity']
            ordered_packages_map[product_id][delivery_date] += quantity

        allocations = []

        for product_id in product_ids:
            product = products.get(product_id)
            if not product:
                continue

            packages_by_date = {}
            for dt in self._iter_workdays(start_date, delivery_date):
                packages_by_date[dt] = ordered_packages_map[product_id][dt]

            total_packages = sum(packages_by_date.values())
            batches_required = math.ceil(total_packages / product.batch_packages)

            allocated_batches = 0
            packages_allocated = 0
            current_date = start_date

            while current_date <= delivery_date and allocated_batches < batches_required:
                if current_date.weekday() >= 5:
                    current_date += timedelta(days=1)
                    continue

                daily_capacity = math.floor(product.daily_batch_capacity * 0.7)
                used_capacity = production_map[product_id][current_date]
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

                    used = production_map[product_id][check_date]
                    if used + batches_today > daily_capacity:
                        can_fit_batch = False
                        break

                if can_fit_batch:
                    packages_remaining = total_packages - packages_allocated

                    if (batches_required - allocated_batches) == batches_today:
                        packages_today = packages_remaining
                    else:
                        packages_today = min(packages_remaining, batches_today * product.batch_packages)

                    for offset in range(product.batch_production_days):
                        prod_date = current_date + timedelta(days=offset)
                        production_map[product_id][prod_date] += batches_today
                        allocations.append({
                            "product_id": str(product_id),
                            "production_date": prod_date,
                            "batches": batches_today,
                            "packages": packages_today
                        })
                    allocated_batches += batches_today
                    packages_allocated += packages_today
                else:
                    current_date += timedelta(days=1)

            if allocated_batches < batches_required:
                raise ValidationError(
                    f"Unable to allocate production for product {product.name} by delivery date."
                )

        return allocations
    
    def get_production(self):
        summary = {}
        tomorrow = timezone.now() + timedelta(days=1)

        schedules = self.__repository.filter_by_date(tomorrow)
        for sched in schedules:
            product = sched.product
            summary[product.id] = {
                'product_name': product.name,
                'total_batches': sched.batches,
                'total_packages': sched.packages
            }

        return summary
        
    def _iter_workdays(self, start, end):
        current = start
        while current <= end:
            if current.weekday() < 5:
                yield current
            current += timedelta(days=1)
import uuid
import math
from datetime import timedelta
from collections import defaultdict

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.core.services import ServiceBase
from apps.logistics.repositories import ProductionScheduleRepository


class ProductionScheduleService(metaclass=ServiceBase):
    def __init__(
            self, 
            repository=ProductionScheduleRepository()
        ):

        self.__repository = repository
    
    def validate_production(self, products_data, products_obj, delivery_date):
        start_date = timezone.now().date() + timedelta(days=1)
        product_ids = list(set([uuid.UUID(str(item['product_id'])) for item in products_data]))

        production_map = defaultdict(lambda: defaultdict(int))
        schedules = self.__repository.filter(product_ids=product_ids, reference_date=start_date)

        for item in schedules:
            production_map[item.product_id][item.production_date] += item.batches

        ordered_packages_map = defaultdict(lambda: defaultdict(int))
        for item in products_data:
            product_id = uuid.UUID(str(item['product_id']))
            ordered_packages_map[product_id][delivery_date] += item['quantity']

        allocations = []
        workdays = list(self._iter_workdays(start_date, delivery_date))
        
        for product_id in product_ids:
            product = products_obj[product_id]
            
            total_packages = ordered_packages_map[product_id][delivery_date]
            batches_required = math.ceil(total_packages / product.batch_packages)
            
            allocated_batches = 0
            packages_allocated = 0
            
            for current_date in workdays:
                if allocated_batches >= batches_required:
                    break
                    
                available_capacity = product.daily_batch_capacity - production_map[product_id][current_date]
                if available_capacity <= 0:
                    continue

                batches_today = min(available_capacity, batches_required - allocated_batches)
                
                if not self._can_fit_production(product, current_date, batches_today, production_map, delivery_date, workdays):
                    continue

                packages_remaining = total_packages - packages_allocated
                if allocated_batches + batches_today == batches_required:
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

            if allocated_batches < batches_required:
                raise ValidationError(f"Unable to allocate production for product {product.name} by delivery date.")

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
    
    def _can_fit_production(self, product, start_date, batches, production_map, delivery_date, workdays):
        for offset in range(product.batch_production_days):
            check_date = start_date + timedelta(days=offset)
            
            if check_date > delivery_date or check_date not in workdays:
                return False
                
            used_capacity = production_map[product.id][check_date]
            if used_capacity + batches > product.daily_batch_capacity:
                return False
        
        return True
        
    def _iter_workdays(self, start, end):
        current = start
        while current <= end:
            if current.weekday() < 5:
                yield current
            current += timedelta(days=1)
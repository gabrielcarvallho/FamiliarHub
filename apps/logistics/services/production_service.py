import math
from datetime import timedelta
from django.utils import timezone

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
    
    def calculate_production(self, remaining_data):
        start_date = timezone.now().date() + timedelta(days=1)
        product_ids = list(remaining_data.keys())

        products = self.__product_repository.filter_by_id(product_ids)
        schedule = self.__repository.filter(
            product_ids=product_ids,
            reference_date=start_date
        )

        product_schedule = {}
        for data in schedule:
            product_schedule[data.product.id] = data

        for product_id, packages in remaining_data.items():
            product = products.get(id=product_id)
            batches_required = math.ceil(packages / product.batch_packages)

            if product.batch_production_days > 1:
                days_production = math.ceil(batches_required / product.daily_batch_capacity) + (product.batch_production_days - 1)
            else:
                days_production = math.ceil(batches_required / product.daily_batch_capacity)
    
    def schedule_production(self, product, required_packages, delivery_date):
        pass
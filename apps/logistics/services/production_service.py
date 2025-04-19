from apps.core.services import ServiceBase
from apps.logistics.repositories import ProductionScheduleRepository


class ProductionScheduleService(metaclass=ServiceBase):
    def __init__(self, repository=ProductionScheduleRepository()):
        self.__production_repository = repository
    
    def calculate_production(self, product, required_packages, delivery_date):
        pass
    
    def schedule_production(self, product, required_packages, delivery_date):
        pass
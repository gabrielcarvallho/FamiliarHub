from rest_framework.exceptions import ValidationError, NotFound

from apps.core.services import ServiceBase
from apps.products.repositories import ProductRepository
from apps.stock.repositories import StockConfigurationRepository


class StockConfigurationService(metaclass=ServiceBase):
    def __init__(
            self, 
            repository=StockConfigurationRepository(),
            product_repository=ProductRepository()
        ):

        self.__repository = repository
        self.__product_repository = product_repository
    
    def get_configuration(self, configuration_id):
        if not self.__repository.exists_by_id(configuration_id):
            raise NotFound('Stock configuration not found.')
        
        return self.__repository.get_by_id(configuration_id)
    
    def get_all_configurations(self):
        return self.__repository.get_all()
    
    def create_configuration(self, **data):
        product_id = data.get('product_id')

        if self.__repository.exists_by_product_id(product_id):
            raise ValidationError('This product already has a stock configuration.')
        
        if not self.__product_repository.exists_by_id(product_id):
            raise NotFound('Product not found.')
        
        self.__repository.create(data)
    
    def update_configuration(self, obj, **data):
        for attr, value in data.items():
            setattr(obj, attr, value)

        self.__repository.save(obj)
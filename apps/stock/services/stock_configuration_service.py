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

        if not self.__product_repository.exists_by_id(product_id):
            raise NotFound('Product not found.')

        if self.__repository.exists_by_product_id(product_id):
            raise ValidationError('This product already has a stock configuration.')
        
        # product = self.__product_repository.get_by_id(product_id)
        # if not product.is_active:
        #     raise ValidationError('Cannot add a stock configuration for an inactive product.')
        
        self.__repository.create(data)
    
    def update_configuration(self, obj, **data):
        for attr, value in data.items():
            setattr(obj, attr, value)

        self.__repository.save(obj)
    
    def validate_current_stock(self, obj, products_data):
        insufficient_stock = []
        products_without_config = []

        for item in products_data:
            product_id = item['product_id']
            product = obj[product_id]

            if not hasattr(product, 'stock_settings') or not product.stock_settings:
                products_without_config.append(product.name)
                continue

        if products_without_config:
            raise ValidationError(
                f"Produtos sem configuração de estoque: {', '.join(products_without_config)}"
            )
 
    def consume_stock(self, obj, products_data):
        for item in products_data:
            product_id = item['product_id']
            quantity = item['quantity']
            product = obj[product_id]

            stock_config = product.stock_settings
            stock_config.current_stock -= quantity
            stock_config.save(update_fields=['current_stock', 'updated_at'])
    
    def replenish_stock(self, production_items):
        for item in production_items:
            stock_config = item.product.stock_settings
            stock_config.current_stock += item.quantity_produced

            stock_config.save(update_fields=['current_stock', 'updated_at'])
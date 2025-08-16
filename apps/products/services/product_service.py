from rest_framework.exceptions import NotFound

from apps.core.services import ServiceBase
from apps.products.repositories import ProductRepository
from apps.stock.repositories import StockConfigurationRepository


class ProductService(metaclass=ServiceBase):
    def __init__(
            self, 
            repository=ProductRepository(),
            stock_repository=StockConfigurationRepository()
        ):

        self.__repository = repository
        self.__stock_repository = stock_repository
    
    def get_product(self, product_id):
        if not self.__repository.exists_by_id(product_id):
            raise NotFound("Product not found.")
        
        return self.__repository.get_by_id(product_id)
    
    def get_all_products(self):
        return self.__repository.get_all()
    
    def get_active_products(self):
        return self.__repository.get_active()
    
    def get_inactive_products(self):
        return self.__repository.get_inactive()
    
    def create_product(self, **data):
        self.__repository.create(data)
    
    def update_product(self, obj, **data):
        for attr, value in data.items():
            setattr(obj, attr, value)

        self.__repository.save(obj)
    
    def delete_product(self, product_id):
        if not self.__repository.exists_by_id(product_id):
            raise NotFound("Product not found.")
        
        self.__repository.soft_delete(product_id)

        if self.__stock_repository.exists_by_product_id(product_id):
            self.__stock_repository.soft_delete(product_id)
import uuid
from rest_framework.exceptions import NotFound

from apps.core import ServiceBase
from apps.products.repositories import ProductRepository


class ProductService(metaclass=ServiceBase):
    def __init__(self, repository=ProductRepository()):
        self.__repository = repository
    
    def get_product(self, product_id):
        if not self.__repository.exists_by_id(product_id):
            raise NotFound("Product not found.")
        
        return self.__repository.get_by_id(product_id)
    
    def get_all_products(self):
        products = self.__repository.get_all()
        if not products:
            raise NotFound('No products found.')
        
        return products
    
    def create_product(self, **data):
        return self.__repository.create(data)
    
    def update_product(self, obj, **data):
        for attr, value in data.items():
            setattr(obj, attr, value)

        self.__repository.save(obj)
        return obj
    
    def delete_product(self, product_id):
        if not self.__repository.exists_by_id(product_id):
            raise NotFound("Product not found.")
        
        self.__repository.delete(product_id)
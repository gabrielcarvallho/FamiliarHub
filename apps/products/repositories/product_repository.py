import uuid
from apps.products.models import Product


class ProductRepository:
    def exists_by_id(self, product_id: uuid.UUID) -> bool:
        return Product.objects.filter(id=product_id).exists()
    
    def get_by_id(self, product_id: uuid.UUID) -> Product:
        return Product.objects.get(id=product_id)
    
    def get_all(self) -> list[Product]:
        return Product.objects.all()
    
    def create(self, product_data: dict) -> Product:
        return Product.objects.create(**product_data)

    def delete(self, product_id: uuid.UUID) ->  None:
        Product.objects.filter(id=product_id).delete()
    
    def save(self, obj: Product) -> Product:
        obj.save()
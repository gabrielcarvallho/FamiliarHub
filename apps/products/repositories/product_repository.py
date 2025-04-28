import uuid
from django.db.models import QuerySet
from apps.products.models import Product


class ProductRepository:
    def exists_by_id(self, product_id: uuid.UUID) -> bool:
        return Product.objects.filter(id=product_id).exists()
    
    def get_existing_ids(self, product_ids: list[uuid.UUID]):
        return Product.objects.filter(id__in=product_ids).values_list('id', flat=True)
    
    def get_by_id(self, product_id: uuid.UUID) -> QuerySet[Product]:
        return Product.objects.get(id=product_id)
    
    def get_all(self) -> QuerySet[Product]:
        return Product.objects.all().order_by('name')
    
    def filter_by_id(self, product_ids: list[uuid.UUID])  -> QuerySet[Product]:
        return Product.objects.filter(id__in=product_ids).order_by('name')
    
    def create(self, product_data: dict) -> QuerySet[Product]:
        return Product.objects.create(**product_data)

    def delete(self, product_id: uuid.UUID) ->  None:
        Product.objects.filter(id=product_id).delete()
    
    def save(self, obj: Product) -> None:
        obj.save()
import uuid
from apps.customers.models import Customer


class CustomerRepository:
    def exists_by_id(self, customer_id: uuid.UUID) -> bool:
        return Customer.objects.filter(id=customer_id).exists()
    
    def exists_by_cnpj(self, cnpj: str) -> bool:
        return Customer.objects.filter(cnpj=cnpj).exists()
    
    def get_by_id(self, customer_id: uuid.UUID) -> Customer:
        return Customer.objects.get(id=customer_id)
    
    def get_all(self) -> list[Customer]:
        return Customer.objects.all()
    
    def create(self, customer_data: dict) -> Customer:
        return Customer.objects.create(**customer_data)
    
    def delete(self, customer_id: uuid.UUID) -> None:
        Customer.objects.filter(id=customer_id).delete()
    
    def save(self, obj: Customer) -> None:
        obj.save()
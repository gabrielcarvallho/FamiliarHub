import uuid
from django.db.models import Prefetch, QuerySet
from apps.customers.models import Customer, Address


class CustomerRepository:
    def exists_by_id(self, customer_id: uuid.UUID) -> bool:
        return Customer.objects.filter(id=customer_id).exists()
    
    def exists_by_cnpj(self, cnpj: str) -> bool:
        return Customer.objects.filter(cnpj=cnpj).exists()
    
    def get_by_id(self, customer_id: uuid.UUID) -> QuerySet[Customer]:
        return Customer.objects.prefetch_related('contact', 'addresses').get(id=customer_id)
    
    def get_all(self) -> QuerySet[Customer]:
        return Customer.objects.prefetch_related(
            'contact',
            Prefetch(
                'addresses',
                queryset=Address.objects.filter(is_billing_address=True),
                to_attr='billing_address'
            )
        ).all().order_by('company_name')
    
    def filter(self, **params):
        return Customer.objects.filter(**params)

    def filter_by_address(self, customer_id: uuid.UUID) -> QuerySet[Customer]:
        return Customer.objects.prefetch_related(
            'contact',
            Prefetch(
                'addresses',
                queryset=Address.objects.filter(is_billing_address=True),
                to_attr='billing_address'
            )
        ).get(id=customer_id)

    def create(self, customer_data: dict) -> QuerySet[Customer]:
        return Customer.objects.create(**customer_data)
    
    def delete(self, customer_id: uuid.UUID) -> None:
        Customer.objects.filter(id=customer_id).delete()
    
    def save(self, obj: Customer) -> None:
        obj.save()
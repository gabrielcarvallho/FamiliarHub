import uuid
from django.db.models import QuerySet
from apps.orders.models import Payment


class PaymentRepository:
    def exists_by_id(self, payment_id: uuid.UUID) -> bool:
        return Payment.objects.filter(id=payment_id).exists()
    
    def get_by_id(self, payment_id: uuid.UUID) -> QuerySet[Payment]:
        return Payment.objects.get(id=payment_id)
    
    def get_all(self) -> QuerySet[Payment]:
        return Payment.objects.all()
    
    def create(self, payment_data: dict) -> QuerySet[Payment]:
        Payment.objects.create(**payment_data)
    
    def delete(self, payment_id: uuid.UUID) -> None:
        Payment.objects.filter(id=payment_id).delete()
    
    def save(self, obj: Payment) -> None:
        obj.save()
import uuid
from django.db.models import QuerySet
from apps.orders.models import Payment


class PaymentRepository:
    def exists_by_id(self, payment_id: uuid.UUID):
        return Payment.objects.filter(id=payment_id).exists()
    
    def get_all(self) -> QuerySet[Payment]:
        return Payment.objects.all()
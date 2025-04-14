from apps.orders.models import Payment


class PaymentRepository:
    def get_all(self):
        return Payment.objects.all()
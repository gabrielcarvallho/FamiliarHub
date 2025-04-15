from apps.orders.models import Status


class StatusRepository:
    def get_all(self):
        return Status.objects.all()
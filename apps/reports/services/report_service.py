from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.core.services import ServiceBase
from apps.accounts.repositories import UserRepository
from apps.customers.repositories import CustomerRepository
from apps.orders.repositories.order_repository import OrderRepository


class ReportService(metaclass=ServiceBase):
    def __init__(
            self,
            user_repository=UserRepository(),
            order_repository=OrderRepository(),
            customer_repository=CustomerRepository()
        ):

        self.__user_repository = user_repository
        self.__order_repository = order_repository
        self.__customer_repository = customer_repository

    def get_reports(self, days):
        if days <= 0:
            raise ValidationError('Number of days must be greater than zero.')

        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)

        orders = self.__order_repository.filter(
            created_at__range=(start_date, end_date)
        )

        customers = self.__customer_repository.filter(
            created_at__range=(start_date, end_date)
        )

        users = self.__user_repository.get_all()

        total_users = users.count()
        total_sales = orders.count()
        total_customers = customers.count()

        total_value = sum(order.total_price for order in orders)

        return {
            'total_sales': total_sales,
            'total_value': total_value,
            'total_customers': total_customers,
            'active_users': total_users,
            'start_date': start_date.date(),
            'end_date': end_date.date(),
        }
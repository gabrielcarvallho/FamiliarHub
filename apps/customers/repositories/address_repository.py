from apps.customers.models import Address


class AddressRepository:
    def create(self, address_data: dict) -> Address:
        return Address.objects.create(**address_data)
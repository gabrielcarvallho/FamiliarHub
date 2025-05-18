from apps.core.services import ServiceBase
from apps.orders.repositories import StatusRepository


class StatusService(metaclass=ServiceBase):
    def __init__(self, repository=StatusRepository()):
        self.__repository = repository

    def get_all_status(self):
        return self.__repository.get_all()
from rest_framework.exceptions import PermissionDenied

from apps.core.services import ServiceBase
from apps.accounts.repositories import GroupRepository


class GroupService(metaclass=ServiceBase):
    def __init__(
            self,
            repository=GroupRepository()
        ):

        self.__group_repository = repository

    def get_all_groups(self, request):
        if not request.user.is_admin:
            raise PermissionDenied('You do not have permission to access this resource.')

        return self.__group_repository.get_all()
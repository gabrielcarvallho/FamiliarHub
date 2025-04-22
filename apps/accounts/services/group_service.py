from apps.core.services import ServiceBase
from apps.accounts.repositories import GroupRepository

from rest_framework.exceptions import PermissionDenied, NotFound


class GroupService(metaclass=ServiceBase):
    def __init__(self):
        self.group_repository = GroupRepository()

    def get_all_groups(self, request):
        if not request.user.is_admin:
            raise PermissionDenied('You do not have permission to access this resource.')
        
        groups = self.group_repository.get_all()
        if not groups:
            raise NotFound('No groups found.')

        return list(groups)
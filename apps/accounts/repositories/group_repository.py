import uuid
from django.db.models import QuerySet
from apps.accounts.models import Group


class GroupRepository:
    def exists_by_id(self, group_id: uuid.UUID) -> bool:
        return Group.objects.filter(id=group_id).exists()
    
    def get_all(self) -> QuerySet[Group]:
        return Group.objects.exclude(name='admin').all()
    
    def get_admin_group(self) -> QuerySet[Group]:
        return Group.objects.get(name='admin')
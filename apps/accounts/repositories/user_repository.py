import uuid
from apps.accounts.models import CustomUser, Group


class UserRepository:
    def exists_by_id(self, user_id: uuid.UUID) -> bool:
        return CustomUser.objects.filter(id=user_id).exists()
    
    def get_by_id(self, user_id: uuid.UUID) -> CustomUser:
        return CustomUser.objects.get(id=user_id)
        
    def get_all(self) -> list[CustomUser]:
        return CustomUser.objects.all().order_by('date_joined')
    
    def create(self, user_data: dict) -> CustomUser:
        return CustomUser.objects.create_user(**user_data)
    
    def delete(self, user_id: uuid.UUID) -> None:
        CustomUser.objects.filter(id=user_id).delete()
    
class GroupRepository:
    def exists_by_id(self, group_id: uuid.UUID) -> bool:
        return Group.objects.filter(id=group_id).exists()
    
    def get_all(self) -> list[Group]:
        return Group.objects.exclude(name='admin').all()
    
    def get_admin_group(self) -> Group:
        return Group.objects.get(name='admin')
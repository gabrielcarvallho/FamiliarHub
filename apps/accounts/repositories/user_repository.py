import uuid
from django.db.models import QuerySet
from apps.accounts.models import CustomUser


class UserRepository:
    def exists_by_id(self, user_id: uuid.UUID) -> bool:
        return CustomUser.objects.filter(id=user_id).exists()
    
    def exists_by_email(self, email: str) -> bool:
        return CustomUser.objects.filter(email=email).exists()
    
    def get_by_id(self, user_id: uuid.UUID) -> QuerySet[CustomUser]:
        return CustomUser.objects.get(id=user_id)
        
    def get_all(self) -> QuerySet[CustomUser]:
        return CustomUser.objects.all().order_by('date_joined')
    
    def create(self, user_data: dict) -> QuerySet[CustomUser]:
        return CustomUser.objects.create_user(**user_data)
    
    def delete(self, user_id: uuid.UUID) -> None:
        CustomUser.objects.filter(id=user_id).delete()
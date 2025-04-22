import uuid
from django.db.models import QuerySet
from apps.accounts.models import CustomUserInvitation


class UserInvitationRepository:
    def exists_by_email(self, email: str) -> bool:
        return CustomUserInvitation.objects.filter(email=email).exists()
    
    def get_by_email(self, email: str) -> QuerySet[CustomUserInvitation]:
        return CustomUserInvitation.objects.get(email=email)

    def create(self, data: dict) -> QuerySet[CustomUserInvitation]:
        return CustomUserInvitation.objects.create(**data)
    
    def delete(self, invite_id: uuid.UUID) -> None:
        CustomUserInvitation.objects.filter(id=invite_id).delete()
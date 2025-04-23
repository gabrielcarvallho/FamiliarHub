import uuid
from datetime import timedelta
from django.utils import timezone
from django.db.models import QuerySet
from apps.accounts.models import CustomUserInvitation


class UserInvitationRepository:
    def exists_by_email(self, email: str) -> bool:
        return CustomUserInvitation.objects.filter(email=email).exists()
    
    def exists_by_token(self, token: str) -> bool:
        return CustomUserInvitation.objects.filter(token=token).exists()
    
    def get_by_email(self, email: str) -> QuerySet[CustomUserInvitation]:
        return CustomUserInvitation.objects.get(email=email)
    
    def get_by_token(self, token: str) -> QuerySet[CustomUserInvitation]:
        return CustomUserInvitation.objects.get(token=token)
    
    def get_not_accepted(self, created_by_id: uuid.UUID) -> QuerySet[CustomUserInvitation]:
        return CustomUserInvitation.objects.filter(
            created_by_id=created_by_id,
            accepted=False
        ).order_by('-created_at')

    def create(self, data: dict) -> QuerySet[CustomUserInvitation]:
        return CustomUserInvitation.objects.create(**data)
    
    def update(self, obj: CustomUserInvitation) -> QuerySet[CustomUserInvitation]:
        obj.token = uuid.uuid4().hex
        obj.expire_at = timezone.now() + timedelta(hours=48)

        obj.save()
        return obj
    
    def mark_as_accepted(self, obj: CustomUserInvitation) -> None:
        obj.accepted = True
        obj.save()
    
    def delete(self, invitation_id: uuid.UUID) -> None:
        CustomUserInvitation.objects.filter(id=invitation_id).delete()
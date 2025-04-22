from apps.core.services import ServiceBase
from apps.accounts.repositories import UserRepository, UserInvitationRepository, GroupRepository

from rest_framework.exceptions import ValidationError, NotFound


class UserInvitationService(metaclass=ServiceBase):
    def __init__(
            self,
            repository=UserInvitationRepository(),
            user_repository=UserRepository(),
            group_repository=GroupRepository()
        ):
        
        self.__repository = repository
        self.__user_repository = user_repository
        self.__group_repository = group_repository
        
    def create_invite(self, created_by, **data):
        email = data.get('email')
        group_id = data.get('group_id', None)
        is_admin = data.pop('is_admin', None)

        if self.__user_repository.exists_by_email(email):
            raise ValidationError('This email is already in use.')
        
        if self.__repository.exists_by_email(email):
            existing_invitation = self.__repository.get_by_email(email)

            if existing_invitation.is_expired:
                self.__repository.delete(existing_invitation.id)
            else:
                raise ValidationError('There is already a pending invitation for this email.')
        
        if not is_admin and not self.__group_repository.exists_by_id(group_id):
            raise NotFound('Group not found.')
        
        data['created_by_id'] = created_by.id
        invitation = self.__repository.create(data)

        return invitation.token
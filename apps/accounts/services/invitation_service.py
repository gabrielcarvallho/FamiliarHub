from django.db import transaction

from apps.core.services import ServiceBase, EmailService
from apps.accounts.repositories import UserRepository, UserInvitationRepository, GroupRepository

from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound


class UserInvitationService(metaclass=ServiceBase):
    def __init__(
            self,
            repository=UserInvitationRepository(),
            user_repository=UserRepository(),
            group_repository=GroupRepository(),

            email_service=EmailService()
        ):
        
        self.__repository = repository
        self.__user_repository = user_repository
        self.__group_repository = group_repository

        self.__email_service = email_service
    
    def get_invitation(self, token):
        if not self.__repository.exists_by_token(token):
            raise ValidationError('Invitation not found.')
        
        return self.__repository.get_by_token(token)
    
    def get_not_accepted(self, request):
        return self.__repository.get_not_accepted(request.user.id)

    @transaction.atomic  
    def create_invitation(self, created_by, **data):
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
                raise ValidationError('There is already a invitation for this email.')
        
        if not is_admin and not self.__group_repository.exists_by_id(group_id):
            raise NotFound('Group not found.')
        
        data['created_by_id'] = created_by.id
        invitation = self.__repository.create(data)

        self.__email_service.send_invitation_email(email, invitation.token)

    def resend_invitation(self, invitation, request):
        if not invitation.created_by.id == request.user.id:
            raise PermissionDenied('You do not have permission to access this resource.')
        
        if invitation.accepted:
            raise ValidationError('Invitation link has already been accepted.')
        
        self.__repository.update(invitation)
        self.__email_service.send_invitation_email(invitation.email, invitation.token)
    
    @transaction.atomic
    def accept_invitation(self, token, **data):
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.pop('confirm_password')

        if not self.__repository.exists_by_token(token):
            raise NotFound('Invitation not found.')
        
        invitation = self.__repository.get_by_token(token)

        if invitation.accepted:
            raise ValidationError('The invitation has already been accepted.')
        
        if invitation.is_expired:
            self.__repository.delete(invitation.id)
            raise ValidationError('Invitation expired.')
        
        if email != invitation.email:
            raise ValidationError('E-mail addresses do not match.')

        if confirm_password != password:
            raise ValidationError('Passwords do not match.')
        
        if not invitation.group:
            data['is_admin'] = True
        
        user = self.__user_repository.create(data)

        if invitation.group:
            user.groups.set([invitation.group])
            
        self.__repository.mark_as_accepted(invitation)
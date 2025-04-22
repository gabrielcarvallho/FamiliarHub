import jwt
from datetime import timedelta
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.core.services import ServiceBase
from apps.accounts.repositories import UserRepository, GroupRepository

from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError


class UserService(metaclass=ServiceBase):
    def __init__(
            self,
            repository=UserRepository(),
            group_repository=GroupRepository()
        ):

        self.__repository = repository
        self.__group_repository = group_repository

    def get_user(self, request, user_id=None):
        if user_id:
            if not request.user.is_admin:
                raise PermissionDenied('You do not have permission to access this resource.')
            
            if not self.__repository.exists_by_id(user_id):
                raise NotFound('User not found.')

            return self.__repository.get_by_id(user_id)
        else:
            return request.user
    
    def get_all_users(self, request):
        if not request.user.is_admin:
            raise PermissionDenied('You do not have permission to access this resource.')

        return self.__repository.get_all()

    def invite_user(self, data):
        email = data.get('email')
        is_admin = data.get('is_admin', False)
        group = data.pop('group', None)
        
        payload = {
            'is_admin': is_admin,
            'exp': timezone.now() + timedelta(hours=5),
            **({'group': group.id} if not is_admin else {})
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        self.email_service.send_invitation_email(email, token)

    @transaction.atomic
    def create_user(self, **data):
        is_admin = data.get('is_admin', False)
        group = data.pop('group', None)

        if is_admin:
            group = self.group_repository.get_admin_group()
        else:
            if group.name == 'admin':
                raise ValidationError('Non-admin users cannot be assigned to the admin group.')

        user = self.user_repository.create(data)
        user.groups.set([group])
        
        return user
    
    def delete_user(self, user_id):
        if not self.user_repository.exists_by_id(user_id):
            raise NotFound('User not found.')

        self.user_repository.delete(user_id)
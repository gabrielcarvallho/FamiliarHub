from django.db import transaction
from apps.core.services.base_service import ServiceBase
from apps.accounts.repositories.repository import UserRepository, GroupRepository

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from rest_framework.exceptions import PermissionDenied, NotFound, AuthenticationFailed, ValidationError


class AuthService(metaclass=ServiceBase):
    def logout(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            raise AuthenticationFailed('No refresh token provided.')
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as e:
            raise AuthenticationFailed('Invalid refresh token.')

class UserService(metaclass=ServiceBase):
    def __init__(self):
        self.user_repository = UserRepository()
        self.group_repository = GroupRepository()

    def get_user_by_id(self, request, user_id=None):
        if user_id:
            if not request.user.is_admin:
                raise PermissionDenied('You do not have permission to access this resource.')
            
            if not self.user_repository.exists_by_id(user_id):
                raise NotFound('User not found.')

            return self.user_repository.get_by_id(user_id)
        else:
            return request.user
    
    def get_all_users(self, request):
        if not request.user.is_admin:
            raise PermissionDenied('You do not have permission to access this resource.')
        
        users = self.user_repository.get_all()
        if not users:
            raise NotFound('No users found.')

        return users
    
    @transaction.atomic
    def create_user(self, data):
        is_admin = data.get('is_admin', False)
        group = data.pop('group', None)

        if is_admin:
            group = self.group_repository.get_admin_group()
        else:
            if not group:
                raise ValidationError("A group is required when is_admin is False.")
            
            if group.name == 'admin':
                raise ValidationError("Non-admin users cannot be assigned to the admin group.")

        user = self.user_repository.create(data)
        user.groups.set([group])
        
        return user
    
    def delete_user(self, user_id):
        if not self.user_repository.exists_by_id(user_id):
            raise NotFound('User not found.')

        self.user_repository.delete(user_id)

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
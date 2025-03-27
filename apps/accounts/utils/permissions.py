from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        action = {
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete',
            'GET': 'view',
        }.get(request.method, None)

        if not action:
            return False

        return request.user.has_perm(f'accounts.{action}_customuser')
from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        action = {
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete',
            'GET': 'view',
        }.get(request.method, None)

        app_label = view.permission_app_label
        model_name = view.permission_model

        if not action:
            return False
        
        if request.user.is_admin:
            return True

        return request.user.has_perm(f'{app_label}.{action}_{model_name}')

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        
        return obj.created_by.id == request.user.id
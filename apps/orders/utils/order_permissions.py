from rest_framework import permissions


class OrderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='delivery_person'):
            if obj.order_status.identifier == 2:
                return True

        return False
from rest_framework.permissions import BasePermission


class OnlyStaffMemberPermission(BasePermission):
    def has_permission(self, request, view):
        permission = hasattr(request.user, 'staffmember')
        return bool(request.user and request.user.is_authenticated and permission)

from rest_framework.permissions import BasePermission


class OnlyStaffMemberPermission(BasePermission):
    def has_permission(self, request, view):
        permission = hasattr(request.user, 'staffmember')
        return request.user and permission

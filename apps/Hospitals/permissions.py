from rest_framework import permissions

class UnrestrictedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True  # Allow unrestricted access

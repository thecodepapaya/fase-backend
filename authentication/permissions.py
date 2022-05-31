from rest_framework import permissions

class SkipAuth(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return True
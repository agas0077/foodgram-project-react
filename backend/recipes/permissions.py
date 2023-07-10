# Third Party Library
from rest_framework import permissions


class IsRecipeAuthor(permissions.BasePermission):
    """Класс разрешения для Recipe."""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.author == request.user

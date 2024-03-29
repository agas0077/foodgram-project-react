# Third Party Library
from rest_framework import permissions


class RecipePermission(permissions.BasePermission):
    """Пермишен, проверяющий уровни доступа к рецептам."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.author == request.user

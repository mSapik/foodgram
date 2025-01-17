from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Класс разрешений, который предоставляет доступ администраторам,
    автору объекта или разрешает доступ только для чтения для всех остальных.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(
            self, request: Request, view: APIView, obj) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or obj.author == request.user
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Класс разрешений, предоставляет доступ администраторам
    или разрешает доступ только для чтения для всех остальных.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser)
            )
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Класс разрешений, предоставляет доступ автору объекта
    или разрешает доступ только для чтения для всех остальных.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(
            self, request: Request, view: APIView, obj) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
        )

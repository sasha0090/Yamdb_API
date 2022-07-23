from rest_framework import permissions


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Просматривать может любой, а запись только автор или админ с модером"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        return (
            request.method in permissions.SAFE_METHODS
            or user.is_authenticated
            and (obj.author == user or user.is_moderator or user.is_admin)
        )


class IsUserForSelfPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdminOrStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or (
            request.user.is_authenticated and request.user.is_admin
        )

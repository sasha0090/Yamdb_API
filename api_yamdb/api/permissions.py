from rest_framework import permissions

USER_METODS = ("GET", "HEAD", "OPTIONS", "POST", "PATCH")


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


def is_safe_methods(method):
    return method in permissions.SAFE_METHODS


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Просматривать может любой, а запись только автор или админ с модером"""

    def has_permission(self, request, view):
        return is_safe_methods(request.method) or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (is_safe_methods(request.method)
                or user.is_authenticated
                and (obj.author == user or user.is_moderator or user.is_admin))


class IsAdminOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) or (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )

from rest_framework import permissions

USER_METODS = ("GET", "HEAD", "OPTIONS", "POST", "PATCH")


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) or (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class ReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        is_anonimus = request.method in permissions.SAFE_METHODS

        is_user = (
            request.method in USER_METODS
            and request.user
            and request.user.is_authenticated
        )
        is_admin = (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )
        is_moderator = (
            request.user.is_authenticated and request.user.is_moderator
        )
        return is_anonimus or is_user or is_admin or is_moderator


class CommentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS) or (
            obj.author == request.user
            or request.user.is_admin
            or request.user.is_superuser
            or request.user.is_moderator
        )

    def has_permission(self, request, view):
        is_anonimus = request.method in permissions.SAFE_METHODS
        is_user = (
            request.method in USER_METODS
            and request.user
            and request.user.is_authenticated
        )
        is_admin = (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )
        is_moderator = (
            request.user.is_authenticated and request.user.is_moderator
        )
        return is_anonimus or is_user or is_admin or is_moderator

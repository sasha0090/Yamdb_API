from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        return (
            request.method in SAFE_METHODS
            or user.is_authenticated
            and (obj.author == user
                 or user.is_moderator
                 or user.is_admin)
        )

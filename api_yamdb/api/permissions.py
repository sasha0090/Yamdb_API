from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStaff(BasePermission):
    """Сотрудник может менять объект"""

    def has_permission(self, request, view):
        """ user.role user moderator admin """
        # Добавить проверку на сотрудника
        return False


class IsAuthorOrReadOnly(BasePermission):
    """Только автор может менять объект, иначе только чтение"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

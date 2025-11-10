from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProfesorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and getattr(getattr(user, "rol", None), "nombre_rol", "").lower() in ["profesor","admin"])

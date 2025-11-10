# third-party import
from rest_framework.permissions import BasePermission;

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser);
    
    
class IsCollgeAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "collge_admin");
    
class IsTeacherOwner(BasePermission):
    """
    Object-level permission: allows teacher to read/modify their own Teacher profile.
    """
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and obj.user == request.user);
    

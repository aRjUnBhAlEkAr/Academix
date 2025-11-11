# third-party imports
from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsCollegeAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'college_admin')


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'teacher')


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'student')


# Object-level checks
class IsSameCollegeObject:
    """
    Helper mixin to check the request.user.college matches object's college.
    Use in view methods (not as a DRF permission directly).
    """
    @staticmethod
    def same_college(user, obj_college):
        if user.is_superuser:
            return True
        if not getattr(user, 'college', None):
            return False
        return user.college == obj_college

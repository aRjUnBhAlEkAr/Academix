from rest_framework import permissions;

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'superuser');
    
class IsCollegeAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.uset.is_authenticated and request.user.role == 'college_admin');

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.uset.is_authenticated and request.user.role == 'teacher');

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.uset.is_authenticated and request.user.role == 'student');

class IsCollegeAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False;
        return request.user.role in ['college_admin', 'superuser'];
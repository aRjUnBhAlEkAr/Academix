# third-party imports
from rest_framework import viewsets, status;
from rest_framework.response import Response;
from rest_framework.permissions import IsAuthenticated;
from .models import Student;
from .serializers import StudentCreateSerializer, StudentReadSerializer;
from .permissions import IsCollegeAdminOrReadOnly, IsSameCollege;

# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user').all();
    permission_classes = [IsAuthenticated, IsCollegeAdminOrReadOnly, IsSameCollege];
    
    def get_queryset(self):
        user = self.request.user;
        
        if user.role == 'college_admin':
            return Student.objects.filter(user__college=user.college);
        elif user.role == 'teacher':
            return Student.objects.filter(user__college=user.college);
        elif user.role == 'student':
            return Student.objects.filter(user=user);
        
        return Student.objects.none();
    
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StudentCreateSerializer;
        return StudentReadSerializer;
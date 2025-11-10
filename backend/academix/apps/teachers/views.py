# third-party import
from rest_framework import viewsets, status;
from rest_framework.permissions import IsAuthenticated;
from rest_framework.response import Response;
from rest_framework.exceptions import PermissionDenied;

# local imports
from .models import Teacher;
from .serializers import TeacherReadSerializer, TeacherCreateSerializer, TeacherUpdateSerializer;
from .permissions import IsSuperUser, IsCollegeAdmin, IsTeacherOwner;

class TeacherViewSet(viewSets.ModelViewSet):
    queryset = Teacher.objects.select_related('user').all();
    permission_classes = [IsAuthenticated]  # Additional checks inside methods

    def get_queryset(self):
        user = self.request.user
        # Superuser can see all
        if user.is_superuser:
            return Teacher.objects.select_related('user').all()
        # College admin sees teachers in their college
        if user.role == 'college_admin' and user.college:
            return Teacher.objects.filter(user__college=user.college).select_related('user')
        # Teacher sees only their own profile
        if user.role == 'teacher':
            return Teacher.objects.filter(user=user)
        # Others: none
        return Teacher.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return TeacherCreateSerializer
        if self.action in ['update', 'partial_update']:
            return TeacherUpdateSerializer
        return TeacherReadSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.role == 'college_admin'):
            raise PermissionDenied("Only superuser or college admin can create teachers.")

        # If college admin, ensure created teacher is assigned to same college (handled in serializer.create)
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        read_serializer = TeacherReadSerializer(teacher, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if user.is_superuser:
            return super().retrieve(request, *args, **kwargs)

        if user.role == 'college_admin':
            if instance.user.college == user.college:
                return super().retrieve(request, *args, **kwargs)
            raise PermissionDenied("You cannot view teachers from another college.")

        if user.role == 'teacher':
            if instance.user == user:
                return super().retrieve(request, *args, **kwargs)
            raise PermissionDenied("You can only view your own profile.")

        raise PermissionDenied("You do not have permission to view this teacher profile.")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if user.is_superuser:
            return super().update(request, *args, **kwargs)

        if user.role == 'college_admin':
            if instance.user.college == user.college:
                return super().update(request, *args, **kwargs)
            raise PermissionDenied("You cannot modify teachers from another college.")

        if user.role == 'teacher':
            if instance.user == user:
                return super().update(request, *args, **kwargs)
            raise PermissionDenied("You can only modify your own profile.")

        raise PermissionDenied("You do not have permission to modify this teacher profile.")

    def destroy(self, request, *args, **kwargs):
        # Only superuser can delete by default
        if not request.user.is_superuser:
            raise PermissionDenied("Only superuser can delete teacher profiles.")
        return super().destroy(request, *args, **kwargs)
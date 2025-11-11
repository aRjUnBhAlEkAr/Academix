# third-party imports
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404

from .models import (
    Department, Course, Semester, Subject,
    Enrollment, Exam, Mark, Attendance
)
from .serializers import (
    DepartmentSerializer, CourseSerializer, SemesterSerializer, SubjectSerializer,
    EnrollmentSerializer, EnrollmentCreateSerializer, ExamSerializer, MarkSerializer, AttendanceSerializer
)
from .permissions import IsSuperuser, IsCollegeAdmin, IsTeacher, IsStudent, IsSameCollegeObject


# Generic mixin to enforce college scoping
class CollegeScopedViewSet(viewsets.ModelViewSet):
    """
    Base class that scopes queryset by user's college for non-superusers.
    Child classes must set `model_college_attr` to the attribute name on the model that holds the college FK.
    Example: Subject.model_college_attr = 'college'
    """
    model_college_attr = None

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        if getattr(user, 'college', None):
            attr = self.model_college_attr
            if not attr:
                return queryset.none()
            filters = {f"{attr}": user.college}
            return queryset.filter(**filters)
        return queryset.none()


class DepartmentViewSet(CollegeScopedViewSet):
    queryset = Department.objects.select_related('college').all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    model_college_attr = 'college'

    def create(self, request, *args, **kwargs):
        # Only superuser or college_admin can create
        user = request.user
        if not (user.is_superuser or user.role == 'college_admin'):
            raise PermissionDenied("Only superuser or college admin can create departments.")
        # force college if college_admin
        data = request.data.copy()
        if user.role == 'college_admin':
            data['college'] = user.college.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        inst = serializer.save()
        return Response(self.get_serializer(inst).data, status=status.HTTP_201_CREATED)


class CourseViewSet(CollegeScopedViewSet):
    queryset = Course.objects.select_related('college', 'department').all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    model_college_attr = 'college'

    def create(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.role == 'college_admin'):
            raise PermissionDenied("Only superuser or college admin can create courses.")
        data = request.data.copy()
        if user.role == 'college_admin':
            data['college'] = user.college.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        inst = serializer.save()
        return Response(self.get_serializer(inst).data, status=status.HTTP_201_CREATED)


class SemesterViewSet(CollegeScopedViewSet):
    queryset = Semester.objects.select_related('course').all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAuthenticated]
    model_college_attr = 'course__college'

    def create(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.role == 'college_admin'):
            raise PermissionDenied("Only superuser or college admin can create semesters.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Additional validation: ensure course belongs to user's college
        course = serializer.validated_data.get('course')
        if not IsSameCollegeObject.same_college(user, course.college):
            raise PermissionDenied("Course belongs to a different college.")
        inst = serializer.save()
        return Response(self.get_serializer(inst).data, status=status.HTTP_201_CREATED)


class SubjectViewSet(CollegeScopedViewSet):
    queryset = Subject.objects.select_related('course', 'semester', 'teacher').all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    model_college_attr = 'college'

    def create(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.role == 'college_admin'):
            raise PermissionDenied("Only superuser or college admin can create subjects.")
        data = request.data.copy()
        if user.role == 'college_admin':
            data['college'] = user.college.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        inst = serializer.save()
        return Response(self.get_serializer(inst).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        # e.g., assign teacher — ensure teacher belongs to same college
        instance = self.get_object()
        user = request.user
        data = request.data.copy()
        teacher_id = data.get('teacher')
        if teacher_id:
            # fetch teacher user and check college
            TeacherUser = settings.AUTH_USER_MODEL
            # Use ORM to get user record
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                t = User.objects.get(pk=teacher_id)
            except User.DoesNotExist:
                raise ValidationError("Assigned teacher not found.")
            if not IsSameCollegeObject.same_college(user, getattr(t, 'college', None)):
                raise PermissionDenied("Teacher belongs to a different college.")
        return super().partial_update(request, *args, **kwargs)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'subject').all()
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Enrollment.objects.select_related('student', 'subject').all()
        if user.role == 'college_admin':
            return Enrollment.objects.filter(subject__college=user.college)
        if user.role == 'teacher':
            return Enrollment.objects.filter(subject__teacher=user)
        if user.role == 'student':
            # student user -> find student profile
            return Enrollment.objects.filter(student__user=user)
        return Enrollment.objects.none()

    def create(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.role in ['college_admin', 'teacher']):
            raise PermissionDenied("Only superuser, college admin, or subject teacher can enroll students.")
        serializer = EnrollmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Additional: check user permissions (college scope)
        student = serializer.validated_data['student']
        subject = serializer.validated_data['subject']
        if not IsSameCollegeObject.same_college(user, subject.college):
            raise PermissionDenied("Subject belongs to different college.")
        # If teacher: must be teacher of subject
        if user.role == 'teacher' and subject.teacher_id != user.id:
            raise PermissionDenied("Only assigned subject teacher can enroll students in this subject.")
        inst = serializer.save()
        return Response(EnrollmentSerializer(inst).data, status=status.HTTP_201_CREATED)


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related('subject').all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Exam.objects.all()
        if user.role == 'college_admin':
            return Exam.objects.filter(subject__college=user.college)
        if user.role == 'teacher':
            return Exam.objects.filter(subject__teacher=user)
        if user.role == 'student':
            return Exam.objects.filter(subject__enrollments__student__user=user).distinct()
        return Exam.objects.none()

    def create(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.role in ['college_admin', 'teacher']):
            raise PermissionDenied("Only superuser, college admin, or teacher can create exams.")
        # teacher can create only for their subject
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.validated_data['subject']
        if user.role == 'teacher' and subject.teacher_id != user.id:
            raise PermissionDenied("Cannot create exam for a subject you don't teach.")
        inst = serializer.save()
        return Response(self.get_serializer(inst).data, status=status.HTTP_201_CREATED)


class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.select_related('exam', 'student').all()
    serializer_class = MarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Mark.objects.all()
        if user.role == 'college_admin':
            return Mark.objects.filter(exam__subject__college=user.college)
        if user.role == 'teacher':
            return Mark.objects.filter(exam__subject__teacher=user)
        if user.role == 'student':
            return Mark.objects.filter(student__user=user)
        return Mark.objects.none()

    def create(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.role in ['college_admin', 'teacher']):
            raise PermissionDenied("Only superuser, college admin or teacher can add marks.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exam = serializer.validated_data['exam']
        student = serializer.validated_data['student']
        # teacher can only add marks for their subject
        if user.role == 'teacher' and exam.subject.teacher_id != user.id:
            raise PermissionDenied("Cannot grade exam for subject you don't teach.")
        # ensure student is enrolled
        if not Enrollment.objects.filter(student=student, subject=exam.subject, active=True).exists():
            raise ValidationError("Student is not enrolled in this subject.")
        inst = serializer.save()
        return Response(self.get_serializer(inst).data, status=status.HTTP_201_CREATED)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('subject', 'student').all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Attendance.objects.all()
        if user.role == 'college_admin':
            return Attendance.objects.filter(subject__college=user.college)
        if user.role == 'teacher':
            return Attendance.objects.filter(subject__teacher=user)
        if user.role == 'student':
            return Attendance.objects.filter(student__user=user)
        return Attendance.objects.none()

    def create(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.role in ['college_admin', 'teacher']):
            raise PermissionDenied("Only superuser, college admin or teacher can mark attendance.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.validated_data['subject']
        if user.role == 'teacher' and subject.teacher_id != user.id:
            raise PermissionDenied("Only subject teacher can mark attendance for this subject.")
        inst = serializer.save()
        return Response(self.get_serializer(inst).data, status=status.HTTP_201_CREATED)

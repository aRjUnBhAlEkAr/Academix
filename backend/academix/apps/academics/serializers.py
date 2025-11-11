# third-party imports
from rest_framework import serializers

# local imports
from .models import (
    Department, Course, Semester, Subject,
    Enrollment, Exam, Mark, Attendance
)
from django.conf import settings


# Department / Course / Semester / Subject serializers
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'college', 'name', 'code', 'description', 'active']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'college', 'department', 'name', 'code', 'duration_years', 'active']


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'course', 'number', 'start_date', 'end_date', 'active']


class SubjectSerializer(serializers.ModelSerializer):
    # show teacher basic info
    teacher_email = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'college', 'course', 'semester', 'name', 'code', 'credits', 'teacher', 'teacher_email', 'active']
        read_only_fields = ['teacher_email']

    def get_teacher_email(self, obj):
        if obj.teacher:
            return getattr(obj.teacher, 'email', None)
        return None

    def validate(self, data):
        # ensure subject.college matches course.college (if both provided)
        course = data.get('course') or getattr(self.instance, 'course', None)
        college = data.get('college') or getattr(self.instance, 'college', None)
        if course and college and course.college_id != college.id:
            raise serializers.ValidationError("Course and College mismatch.")
        return data


# Enrollment serializer (nested read)
class EnrollmentSerializer(serializers.ModelSerializer):
    student_roll = serializers.SerializerMethodField(read_only=True)
    subject_code = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_roll', 'subject', 'subject_code', 'enrolled_on', 'active']

    def get_student_roll(self, obj):
        return getattr(obj.student, 'roll_number', None)

    def get_subject_code(self, obj):
        return getattr(obj.subject, 'code', None)


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'subject', 'active']

    def validate(self, data):
        # ensure student and subject belong to same college
        student = data.get('student')
        subject = data.get('subject')
        if student and subject:
            student_college = getattr(student.user, 'college', None)
            if student_college != subject.college:
                raise serializers.ValidationError("Student and Subject must belong to same college.")
        return data


# Exam / Mark / Attendance serializers
class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'subject', 'title', 'date', 'max_marks', 'published']


class MarkSerializer(serializers.ModelSerializer):
    student_roll = serializers.SerializerMethodField(read_only=True)
    exam_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Mark
        fields = ['id', 'exam', 'exam_title', 'student', 'student_roll', 'marks_obtained', 'graded_on']

    def get_student_roll(self, obj):
        return getattr(obj.student, 'roll_number', None)

    def get_exam_title(self, obj):
        return getattr(obj.exam, 'title', None)


class AttendanceSerializer(serializers.ModelSerializer):
    student_roll = serializers.SerializerMethodField(read_only=True)
    subject_code = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'subject', 'subject_code', 'student', 'student_roll', 'date', 'present']

    def get_student_roll(self, obj):
        return getattr(obj.student, 'roll_number', None)

    def get_subject_code(self, obj):
        return getattr(obj.subject, 'code', None)

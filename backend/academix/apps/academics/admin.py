from django.contrib import admin

# local imports
from .models import Department, Course, Semester, Subject, Enrollment, Exam, Mark, Attendance

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'college', 'active')
    search_fields = ('name', 'code')
    list_filter = ('active', 'college')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'college', 'department', 'duration_years', 'active')
    search_fields = ('name', 'code')
    list_filter = ('college', 'department', 'active')

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'number', 'start_date', 'end_date', 'active')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'course', 'semester', 'teacher', 'active')
    search_fields = ('name', 'code')
    list_filter = ('course', 'semester', 'active')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'enrolled_on', 'active')
    search_fields = ('student__roll_number', 'subject__code')
    list_filter = ('active',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'title', 'date', 'max_marks', 'published')

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam', 'student', 'marks_obtained', 'graded_on')
    search_fields = ('student__roll_number', 'exam__title')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'student', 'date', 'present')
    list_filter = ('present',)

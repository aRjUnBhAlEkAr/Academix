# django-default imports
from django.contrib import admin

# local-package imports
from .models import Teacher;

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'employee_id', 'department', 'is_active', 'created_at')
    search_fields = ('employee_id', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('department', 'is_active')
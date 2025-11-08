# django default imports
from django.contrib import admin

# local-imports
from .models import Student;

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'roll_number', 'department', 'year', 'is_active')
    search_fields = ('roll_number', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('department', 'year', 'is_active')
    
# django default import
from django.db import models

# importing settings from django.conf.
from django.conf import settings;

# Create your models here.
class Teacher(models.Model):
    """
    Teacher profile linked one-to-one with User (role='teacher').
    Keep profile fields minimal; extend as needed (qualifications, phone, bio).
    """
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            on_delete = models.CASCADE,
            related_name = 'teacher_profile'
        );
    
    employee_id = models.CharField(max_length=50, unique=True);
    department = models.CharField(max_length=100, blank=True);
    hired_date = models.DateField(null=True, blank=True);
    is_active = models.BooleanField(default=True);
    created_at = models.DateTimeField(auto_now_add=True);
    updated_at = models.DateTimeField(auto_now=True);
    
    class Meta:
        ordering = ['-created_at'];
        
    def __str__(self):
        full_name = f"{self.user.first_name} {self.user.last_name}".strip();
        return f"{full_name or self.user.email} ({self.employee_id})";
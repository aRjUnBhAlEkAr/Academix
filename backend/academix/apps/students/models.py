# django default import
from django.db import models

# importing neccessary packages
from django.conf import settings;

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile');
    roll_number = models.CharField(max_length=50, unique=True);
    enrollment_date = models.DateField(auto_now_add=True);
    department = models.CharField(max_length=100, blank=True);
    year = models.PositiveIntegerField(default=1);
    is_active = models.BooleanField(default=True);
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})";
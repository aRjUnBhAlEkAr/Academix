# default django import packages
from django.db import models;

# model specific imports
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin;
from django.utils import timezone;

# Create your models here.
# Below class will manage all users role and their profile
class UserManager(BaseUserManager):
    # it will create a user and by default it would be 'student'
    def create_user(self, email, password=None, role='student', **extra_fields):
        # check if email parameter is not null, otherwise raise error.
        if not email:
            raise ValueError("Email must be set!");
        
        email = self.normalize_email(email);
        user = self.model(email=email, role=role, **extra_fields);
        user.set_password(password);
        user.save(using=self._db);
        return user;
    
    # create a superuser 
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True);
        extra_fields.setdefault('is_superuser', True);
        extra_fields.setdefault('is_active', True);
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have 'is_staff=True'");
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have 'is_superuser=True'");
        
        return self.create_user(email, password, role='superuser', **extra_fields);
    
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('superuser', 'Superuser'),
        ('college_admin', 'College Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ];
    
    email = models.EmailField(unique=True, max_length=255);
    first_name = models.CharField(max_length=150, blank=True);
    last_name = models.CharField(max_length=150, blank=True);
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='student');
    is_staff = models.BooleanField(default=False);
    is_active = models.BooleanField(default=True);
    date_joined = models.DateTimeField(default=timezone.now);
    
    # optional foreign key to college(set by administration app when applicable)
    college = models.ForeignKey('administration.College', null=True, blank=True, on_delete=models.SET_NULL, related_name='users');
    
    # creating object of 'UserManager' class
    objects = UserManager();
    
    USERNAME_FIELD = 'email';
    REQUIRED_FIELD = []
    
    def get_full_name(self):
       return f"{self.first_name} {self.last_name}".strip()
    
    def __str__(self):
        return f"{self.email} ({self.role})";
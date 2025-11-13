from django.db import models
from django.conf import settings;

# Create your models here.
class Department(models.Model):
    college = models.ForeignKey('administration.College', on_delete=models.CASCADE, related_name='departments');

    name = models.CharField(max_length=150);
    code = models.CharField(max_length=50);
    description = models.TextField(blank=True);
    active = models.BooleanField(default=True);
    
    class Meta:
        unique_together = ('college', 'code');
        ordering = ['name'];
    
    def __str__(self):
        return f"{self.name} ({self.code})";
    
class Course(models.Model):
    college = models.ForeignKey('administration.College', on_delete=models.CASCADE, related_name='courses');
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL, related_name='courses');
    name = models.CharField(max_length=200);
    code = models.CharField(max_length=50);
    duration_years = models.PositiveSmallIntegerField(default=3);
    active = models.BooleanField(default=True);
    
    class Meta:
        unique_together = ('college', 'code');
        ordering = ['name'];
        
    def __str__(self):
        return f"{self.name} ({self.code})";
    
class Semester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='semesters');
    number = models.PositiveSmallIntegerField();
    start_date = models.DateField(null=True, blank=True);
    end_date = models.DateField(null=True, blank=True);
    active = models.BooleanField(default=True);
    
    class Meta:
        unique_together = ('course', 'number');
        ordering = ['course', 'number'];
        
    def __str__(self):
        return f"{self.course.code} - Sem {self.number}";
    
class Subject(models.Model):
    college = models.ForeignKey('administration.College', on_delete=models.CASCADE, related_name='subjects');
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects');
    semester = models.ForeignKey(Semester, on_delete= models.CASCADE, related_name='subjects');
    name = models.CharField(max_length=200);
    code = models.CharField(max_length=50);
    
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='subjects');
    active = models.BooleanField(default=True);
    
    class Meta:
        unique_together = ('college', 'code');
        ordering = ['name'];
        
    def __str__(self):
        return f"{self.name} ({self.code})";
    

class Enrollment(models.Model):
    """
    Links a student user to a subject (a student's enrollment in a subject).
    The 'student' FK points to the Student model defined in apps.students.
    We use a lazy reference to avoid circular imports.
    """
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='enrollments');
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments');
    enrolled_on = models.DateField(auto_now_add=True);
    active = models.BooleanField(default=True);
    
    class Meta:
        unique_together = ('student', 'subject');
        ordering = ['-enrolled_on'];
        
    def __str__(self):
        return f"{self.student} -> {self.subject}";
    
class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams');
    title = models.CharField(max_length=200);
    date = models.DateField();
    max_marks = models.PositiveSmallIntegerField(default=100);
    published = models.BooleanField(default=False);
    
    class Meta:
        ordering = ['-date'];
        
    def __str__(self):
        return f"{self.subject.code} - {self.title} ({self.date})";
    
class Mark(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marks');
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='marks');
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2);
    graded_on = models.DateTimeField(auto_now=True);
    
    class Meta:
        unique_together = ('exam', 'student');
        ordering = ['-graded_on'];
        
    def __str__(self):
        return f"{self.student} - {self.exam.title} : {self.marks_obtained}";
    
class Attendance(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendance_records');
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='attendance_records');
    date = models.DateField();
    present = models.BooleanField(default=False);

    class Meta:
        unique_together = ('subject', 'student', 'date');
        ordering = ['-date'];
    
    def __str__(self):
        return f"{self.student} - {self.subject.code} - {self.date} : {'P' if self.present else 'A'}";
    
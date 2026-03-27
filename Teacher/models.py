from django.db import models
from core.models import CustomUser  
from cloudinary.models import CloudinaryField

# COURSE MODEL
class Course(models.Model):
    CATEGORY_CHOICES = [
    ('python', 'Python'),
    ('java', 'Java'),
    ('react', 'React'),
    ('php', 'PHP'),
    ('other', 'Other'), 
]

    name = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='courses',
        limit_choices_to={'role': 'teacher'}
    )
    duration = models.CharField(max_length=50, blank=True)  # e.g., "3 months"
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    syllabus = CloudinaryField('file',resource_type='raw', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
# STUDENT MODEL
class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='student_profile',
        limit_choices_to={'role': 'student'}
    )
    profile_picture = models.ImageField(upload_to='students/', blank=True, null=True)
    enrolled_courses = models.ManyToManyField(Course, related_name='students')
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# ASSIGNMENT MODEL

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    max_marks = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.name})"


class Grade(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='grades')
    score = models.IntegerField()
    total = models.IntegerField(default=100)
    date_recorded = models.DateField()  # NOT auto_now_add

    class Meta:
        unique_together = ('student', 'assignment')  # duplicate grades not allowed

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} - {self.assignment.title}: {self.score}/{self.total}"
# ATTENDANCE MODEL
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} - {self.date}: {self.status}"
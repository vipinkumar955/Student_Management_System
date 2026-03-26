from django.contrib import admin

from django.contrib import admin
from .models import Course, StudentProfile, Assignment, Grade, Attendance

admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Grade)
admin.site.register(Attendance)
admin.site.register(StudentProfile)

from rest_framework import serializers
from .models import Course, StudentProfile, Assignment, Grade, Attendance

# COURSE SERIALIZER
class CourseSerializer(serializers.ModelSerializer):
    syllabus_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'duration', 'category', 'syllabus', 'syllabus_url', 'teacher', 'created_at']
        read_only_fields = ['teacher']

    def get_syllabus_url(self, obj):
        if obj.syllabus:
            return obj.syllabus.url
        return None


# STUDENT SERIALIZER
class StudentProfileSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='user.username', read_only=True)
    enrolled_courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'student_name', 'enrolled_courses', 'date_joined']


# CREATE STUDENT
class CreateStudentSerializer(serializers.ModelSerializer):
    enrolled_courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True)

    class Meta:
        model = StudentProfile
        fields = ['user', 'enrolled_courses']


# ASSIGNMENT SERIALIZER
class AssignmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Assignment
        fields = "__all__"


# GRADE SERIALIZER
class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = Grade
        fields = "__all__"


# ATTENDANCE SERIALIZER
class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Attendance
        fields = "__all__"
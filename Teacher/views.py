from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Course, Assignment, Grade, Attendance, StudentProfile
from .serializers import *
from .permissions import IsTeacherOrAdmin

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Course.objects.all()
        return Course.objects.filter(teacher=user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class AssignmentViewSet(ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]


class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]


class StudentProfileViewSet(ModelViewSet):
    queryset = StudentProfile.objects.all().select_related('user').prefetch_related('enrolled_courses')
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateStudentSerializer
        return StudentProfileSerializer
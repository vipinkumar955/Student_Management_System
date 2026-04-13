from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from .permissions import IsTeacherOrAdmin


#  COURSE
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Course.objects.all()
        return Course.objects.filter(teacher=user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


#  ASSIGNMENT
class AssignmentViewSet(ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Assignment.objects.all()
        return Assignment.objects.filter(course__teacher=user)


# ✅ GRADE 
class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()   #
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Grade.objects.all()
        return Grade.objects.filter(course__teacher=user)


#  ATTENDANCE 
class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()  
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Attendance.objects.all()
        return Attendance.objects.filter(course__teacher=user)


#  STUDENT PROFILE
class StudentProfileViewSet(ModelViewSet):
    queryset = StudentProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateStudentSerializer
        return StudentProfileSerializer
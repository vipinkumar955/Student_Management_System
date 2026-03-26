from django.urls import path
from .views import StudentGradeView, StudentAttendanceView, StudentAssignmentView

urlpatterns = [
    path("grades/", StudentGradeView.as_view()),
    path("attendance/", StudentAttendanceView.as_view()),
    path("assignments/", StudentAssignmentView.as_view()),
]
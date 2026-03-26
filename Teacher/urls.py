from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CourseViewSet,
    AssignmentViewSet,
    GradeViewSet,
    AttendanceViewSet,
    StudentProfileViewSet
)

router = DefaultRouter()
router.register('courses', CourseViewSet)
router.register('assignments', AssignmentViewSet)
router.register('grades', GradeViewSet)
router.register('attendance', AttendanceViewSet)
router.register('students', StudentProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
# Teacher/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from Teacher.models import Grade, StudentProfile, Attendance, Assignment

class StudentGradeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if getattr(user, "role", None) != "student":
            return Response({"error": "Only student allowed"}, status=403)

        try:
            student = StudentProfile.objects.get(user=user)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student profile not found"}, status=404)

        grades = Grade.objects.filter(student=student).select_related("course", "assignment")

        data = [
            {
                "student_name": g.student.user.username,
                "student_id": g.student.id,
                "course": g.course.name if g.course else "",
                "assignment": g.assignment.title if g.assignment else "",
                "score": g.score,
                "total": g.total,
                "date": g.date_recorded.strftime("%Y-%m-%d") if g.date_recorded else ""
            }
            for g in grades
        ]
        return Response(data, status=200)


class StudentAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if getattr(user, "role", None) != "student":
            return Response({"error": "Only student allowed"}, status=403)

        try:
            student = StudentProfile.objects.get(user=user)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student profile not found"}, status=404)

        attendance = Attendance.objects.filter(student=student).select_related("course")

        data = [
            {
                "student_name":a.student.user.username,
                 "student_id": a.student.id,
                "course": a.course.name if a.course else "",
                "date": a.date.strftime("%Y-%m-%d") if a.date else "",
                "status": a.status
            }
            for a in attendance
        ]
        return Response(data, status=200)


class StudentAssignmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if getattr(user, "role", None) != "student":
            return Response({"error": "Only student allowed"}, status=403)

        try:
            student = StudentProfile.objects.get(user=user)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student profile not found"}, status=404)

        assignments = Assignment.objects.filter(student=student).select_related("course")

        data = [
            {
                "student_name": a.student.user.username,
                 "student_id": a.student.id,
                "title": a.title,
                "course": a.course.name if a.course else "",
                "due_date": a.due_date.strftime("%Y-%m-%d") if a.due_date else "",
                "max_marks": a.max_marks
            }
            for a in assignments
        ]
        return Response(data, status=200)
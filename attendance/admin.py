from django.contrib import admin
from django.http import HttpRequest
from course.models import Course
from attendance.models import Attendance


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'student', 'timestamp')
    search_fields = ['id', 'course__course_code', 'course__course_name',
                     'student__institute_email', 'student__name']

    def get_queryset(self, request: HttpRequest):
        user = request.user

        query_set = super().get_queryset(request)

        is_faculty = user.groups.filter(name="Faculty").exists()
        is_student = user.groups.filter(name="Student").exists()

        if is_faculty:
            courses = user.instructors.all()  # Reverse M2M relationship - all courses where user is instructor
            filtered_query_set = query_set.filter(course__in=courses)

        elif is_student:
            filtered_query_set = query_set.filter(student=user)
        else:
            filtered_query_set = query_set

        return filtered_query_set


admin.site.register(Attendance, AttendanceAdmin)

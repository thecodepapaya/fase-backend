from django.contrib import admin

from attendance.models import Attendance


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'student', 'timestamp')
    search_fields = ['id', 'course__course_code', 'course__course_name',
                     'student__institute_email', 'student__name']


admin.site.register(Attendance, AttendanceAdmin)

from django.contrib import admin

from attendance.models import Attendance


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'student', 'timestamp')


admin.site.register(Attendance, AttendanceAdmin)

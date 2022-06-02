from django.contrib import admin

from attendance.models import Attendance, AttendanceAdmin

admin.site.register(Attendance, AttendanceAdmin)

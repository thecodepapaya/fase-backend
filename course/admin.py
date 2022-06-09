from django.contrib import admin

from course.models import Course, CourseWindowRecord


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_code', 'course_name',
                    'semester', 'academic_year',)


class CourseWindowRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'start_timestamp',
                    'attendance_duration_in_minutes',)


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseWindowRecord, CourseWindowRecordAdmin)

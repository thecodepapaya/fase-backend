from django.contrib import admin

from course.models import Course, CourseWindowRecord
from .csv_importer import add_students_from_csv


def populate_students_list_from_csv(modeladmin, request, queryset):

    for course in queryset:
        add_students_from_csv(course, request)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_code', 'course_name', 'section',
                    'semester', 'academic_year', 'is_active',)
    search_fields = ['id', 'course_code', 'course_name', 'section']
    actions = [populate_students_list_from_csv]


class CourseWindowRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'start_timestamp',
                    'attendance_duration_in_minutes',)
    search_fields = ['id', 'course__course_name',
                     'course__course_code', 'course__section']


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseWindowRecord, CourseWindowRecordAdmin)

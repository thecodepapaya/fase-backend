from django.contrib import admin
from django.http import HttpRequest

from course.actions.add_students_from_csv import add_students_from_csv
from course.models import Course, CourseWindowRecord


@admin.action(permissions=['change'])
def populate_students_list_from_csv(modeladmin, request, queryset):

    for course in queryset:
        add_students_from_csv(course, request)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_code', 'course_name', 'section',
                    'semester', 'academic_year', 'is_active',)
    search_fields = ['id', 'course_code', 'course_name', 'section']
    actions = [populate_students_list_from_csv]

    def get_queryset(self, request: HttpRequest):
        user = request.user
        query_set = super().get_queryset(request)

        is_faculty = user.groups.filter(name="Faculty").exists()
        is_student = user.groups.filter(name="Student").exists()

        if is_faculty:
            filtered_data = query_set.filter(instructors=user)

        elif is_student:
            filtered_data = query_set.filter(students=user)

        else:
            filtered_data = query_set

        return filtered_data


class CourseWindowRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'start_timestamp',
                    'attendance_duration_in_minutes',)
    search_fields = ['id', 'course__course_name',
                     'course__course_code', 'course__section']
    raw_id_fields = ('course',)


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseWindowRecord, CourseWindowRecordAdmin)

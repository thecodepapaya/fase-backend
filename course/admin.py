from django.contrib import admin

from course.models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_code', 'course_name',
                    'semester', 'academic_year',)


admin.site.register(Course, CourseAdmin)

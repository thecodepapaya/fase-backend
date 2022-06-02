from django.contrib import admin

from course.models import Course, CourseAdmin

admin.site.register(Course, CourseAdmin)

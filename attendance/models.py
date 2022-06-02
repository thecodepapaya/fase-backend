from course.models import Course
from django.db import models
from registration.models import Registration
from users.models import User
from django.contrib import admin


class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_already_marked(self, request):
        pass

    def __str__(self):
        return str(self.id)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'student', 'timestamp')

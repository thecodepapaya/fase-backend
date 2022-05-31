from course.models import Course
from django.db import models
from registration.models import Registration
from users.models import User


class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)

    def __str__(self):
        return f"Id:{self.attendance_id} Course: {self.course} Student: {self.student}"

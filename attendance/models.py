from django.db import models
from course.models import Course
from registration.models import Registration


class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    registration_data = models.ForeignKey(
        Registration, on_delete=models.CASCADE)

    def __str__(self):
        return "Course: "+str(self.course)+'\nRegistration Details: '+str(self.registration_data)

from course.models import Course
from django.db import models
from registration.models import BasicData, Registration
from students.models import StudentData


class Attendance(BasicData):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    attendance_id = models.AutoField(primary_key=True, unique=True)
    server_key = models.CharField(max_length=40)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return "Course: "+str(self.course)+'\nAttendance Id: '+str(self.attendance_id)


class BleVerification(models.Model):
    # PK (email) of student verifying the attendance
    verified_by = models.EmailField()
    verified_at = models.DateTimeField(auto_now_add=True)
    # PK (id) of attendance
    verified_for = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['verified_by', 'verified_for'], name='unique_verification_per_attendance')]

    def __str__(self):
        return f'Verified by {self.verified_by} at {self.verified_at} for attendance {self.verified_for}'

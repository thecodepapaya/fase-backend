from datetime import datetime

from django.db import models
from users.models import User


def get_academic_year():
    current_year = datetime.now().year
    choices = []
    for year in reversed(range(2020, current_year+1)):
        choices.append((f'{year}-{year+1}', f'{year}-{year+1}'))
    return choices


class Course(models.Model):

    semester_choice = [('autumn', 'Autumn'), ('winter', 'Winter')]

    course_code = models.CharField(max_length=15)
    course_name = models.CharField(max_length=100)
    semester = models.CharField(
        max_length=6, choices=semester_choice, default='autumn')
    academic_year = models.CharField(
        max_length=9, choices=get_academic_year(), default=get_academic_year()[0])
    instructor = models.ManyToManyField(User)
    # The timestamp at which the attendance for this course was last started
    start_timestamp = models.DateTimeField()
    # The duration in minutes for which the attendance window opens for the course
    attendance_duration_in_minutes = models.IntegerField(default=5)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['course_code', 'semester', 'academic_year'], name='course_unique_per_sem_per_year')]

    def __str__(self):
        return f'Course Code: {self.course_code} \nAcademic year: {self.academic_year} \nSemester: {self.semester}'

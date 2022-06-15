import logging
from datetime import datetime

from django.contrib import admin
from django.core.validators import FileExtensionValidator
from django.db import models
from rest_framework.decorators import action
from users.models import User

logger = logging.getLogger(__file__)


def get_academic_year():
    current_year = datetime.now().year
    choices = []
    for year in reversed(range(2020, current_year+1)):
        choices.append((f'{year}-{year+1}', f'{year}-{year+1}'))
    return choices


def get_default_academic_year():
    current_year = datetime.now().year
    academic_year = f'{current_year}-{current_year+1}'

    return academic_year


class Course(models.Model):

    semester_choice = [('autumn', 'Autumn'), ('winter', 'Winter')]

    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    section = models.CharField(max_length=25, null=True, blank=True)
    semester = models.CharField(
        max_length=6, choices=semester_choice, default='autumn')
    academic_year = models.CharField(
        max_length=9, choices=get_academic_year(), default=get_default_academic_year())
    instructors = models.ManyToManyField(
        User, blank=True, related_name='instructors')
    students = models.ManyToManyField(
        User, blank=True, related_name='students')
    # The timestamp at which the attendance for this course was last started
    start_timestamp = models.DateTimeField(null=True, blank=True)
    # The duration in minutes for which the attendance window opens for the course
    attendance_duration_in_minutes = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)

    # The csv which stores a list of students for this course. Adding this file helps populate the `students` field.
    course_student_mapper_file = models.FileField(
        null=True, blank=True, upload_to='student_mapper_csv/', validators=[FileExtensionValidator(allowed_extensions=["csv"])])

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['course_code', 'semester', 'section', 'academic_year'], name='course_unique_per_sem_per_year_per_section'), ]

    def __str__(self):
        return f'{self.course_code}: {self.course_name} (Section: {self.section})'


class CourseWindowRecord(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_timestamp = models.DateTimeField(blank=True, null=True)
    attendance_duration_in_minutes = models.IntegerField(default=5)

    def __str__(self):
        return f'{self.course}'

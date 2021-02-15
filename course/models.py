from django.db import models


class Course(models.Model):
    course_code = models.CharField(max_length=8, primary_key=True)
    course_name = models.CharField(max_length=70)
    instructor_name = models.CharField(max_length=40)
    start_timestamp = models.DateTimeField()

    def __str__(self):
        return 'Course Code: '+self.course_code+'\nCourse Name: '+self.course_name+'\nInstructor Name: '+self.instructor_name

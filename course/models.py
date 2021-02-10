from django.db import models


class Course(models.Model):
    course_code = models.CharField(max_length=6, primary_key=True)
    course_name = models.CharField(max_length=70)
    instructor_name = models.CharField(max_length=34)

    def __str__(self):
        return 'Course Code: '+self.course_code+'\nCourse Name: '+self.course_name+'\nInstructor Name: '+self.instructor_name

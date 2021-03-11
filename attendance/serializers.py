from course.models import Course
from course.serializers import CourseSerializer
from registration.serializers import RegistrationSerializer
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from students.models import StudentData
from students.serializers import StudentDataSerializer

from attendance.models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    student_data = StudentDataSerializer()
    course = CourseSerializer()

    class Meta:
        model = Attendance
        fields = '__all__'

    #TODO: remove get or create with get only
    def to_internal_value(self, data):
        """
            Add foreign key for student data
        """
        student = data.pop('student_data')
        data['student_data'] = StudentData.objects.get_or_create(
            institute_email=student['institute_email'], google_uid=student['google_uid'], name=student['name'])[0]
        """
            Add foreign key for course
        """
        course = data.pop('course')
        data['course'] = Course.objects.get_or_create(
            course_code=course['course_code'], course_name=course['course_name'], instructor_name=course['instructor_name'])[0]
        return data

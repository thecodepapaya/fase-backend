from django.http import Http404
from faculty.models import Faculty
from faculty.serializers import FacultySerializer
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from course.models import Course


class CourseSerializer(serializers.ModelSerializer):
    instructor = FacultySerializer()

    class Meta:
        model = Course
        fields = '__all__'

    def to_internal_value(self, data):
        """
            Add foreign key for instructor
        """
        instructor = data.pop('instructor')
        try:
            data['access_token'] = instructor['access_token']
            data['instructor'] = Faculty.objects.get(
                institute_email=instructor['institute_email'], google_uid=instructor['google_uid'])
        except Faculty.DoesNotExist:
            raise Http404
        return data

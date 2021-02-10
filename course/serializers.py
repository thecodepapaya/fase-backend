from course.models import Course  # , LANGUAGE_CHOICES, STYLE_CHOICES
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

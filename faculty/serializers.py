from faculty.models import Faculty  # , LANGUAGE_CHOICES, STYLE_CHOICES
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework import serializers


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

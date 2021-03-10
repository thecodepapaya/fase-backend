from students.models import StudentData  
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework import serializers


class StudentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = '__all__'

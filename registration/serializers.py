from datetime import datetime
from hashlib import sha1

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from students.models import StudentData
from students.serializers import StudentDataSerializer

from registration.models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    student_data = StudentDataSerializer()

    class Meta:
        model = Registration
        fields = '__all__'

    def to_internal_value(self, data):
        student = data.pop('student_data')
        data['student_data'] = StudentData.objects.get_or_create(
            institute_email=student['institute_email'], google_uid=student['google_uid'], name=student['name'])[0]
        data['server_key'] = sha1(
            str(datetime.now()).encode('utf-8')).hexdigest()
        return data

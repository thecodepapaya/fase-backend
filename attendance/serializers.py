from registration.serializers import RegistrationSerializer
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from attendance.models import Attendance  # , LANGUAGE_CHOICES, STYLE_CHOICES


class AttendanceSerializer(serializers.ModelSerializer):
    registration_data = RegistrationSerializer()

    class Meta:
        model = Attendance
        fields = '__all__'

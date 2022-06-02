import logging

from course.serializers import CourseSerializer
from registration.serializers import RegistrationSerializer
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Attendance

logger = logging.getLogger(__file__)


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

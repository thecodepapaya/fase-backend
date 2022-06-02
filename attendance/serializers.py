import logging

from course.serializers import CourseSerializer
from registration.serializers import RegistrationSerializer
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Attendance

logger = logging.getLogger(__file__)


class AttendanceSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    registration = RegistrationSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ('course', 'student', 'registration',
                  'is_already_marked', 'id', 'timestamp',)

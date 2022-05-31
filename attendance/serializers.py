import logging

from rest_framework import serializers

from .models import Attendance

logger = logging.getLogger(__file__)


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = '__all__'

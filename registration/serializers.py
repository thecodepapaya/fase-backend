import logging

from rest_framework import serializers

from .models import Registration

logger = logging.getLogger(__file__)


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = '__all__'

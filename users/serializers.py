import logging

from rest_framework import serializers

from .models import User

logger = logging.getLogger(__file__)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('institute_email', 'name')

import logging

from rest_framework import serializers

from authentication.models import Token

logger = logging.getLogger(__file__)


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('token',)

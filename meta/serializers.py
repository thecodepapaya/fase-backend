import logging

from rest_framework import serializers

from .models import MetaData

logger = logging.getLogger(__file__)


class MetadataSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetaData
        fields = '__all__'

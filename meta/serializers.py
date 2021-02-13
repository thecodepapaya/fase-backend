from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import MetaData


class MetaDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetaData
        fields = '__all__'

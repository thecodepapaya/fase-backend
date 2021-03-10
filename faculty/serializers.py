from datetime import datetime
from hashlib import sha256

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from faculty.models import Faculty


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

    def to_internal_value(self, data):
        data['access_token'] = sha256(
            str(datetime.now()).encode('utf-8')).hexdigest()
        return data

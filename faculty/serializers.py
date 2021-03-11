import logging
import random
from datetime import datetime
from hashlib import sha256

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from faculty.models import Faculty

logger = logging.getLogger(__file__)


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        exclude = ['access_token']

    def to_internal_value(self, data):
        random_int = random.randint(0, 1000)
        data['access_token'] = sha256(
            (str(random_int)+str(datetime.now())).encode('utf-8')).hexdigest()
        logger.info(f"Generated access_token for data {data}")
        return data

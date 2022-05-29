from django.shortcuts import render

from rest_framework import viewsets
from . import models
from . import serializers


class CourseViewset(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

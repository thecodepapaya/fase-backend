from datetime import timedelta

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course
from .serializers import CourseSerializer


class course_list(APIView):
    def get(self, request, format=None):
        course = Course.objects.filter(start_timestamp__gte=timezone.now(
        )-timedelta(minutes=30)).filter(start_timestamp__lte=timezone.now())
        serializer = CourseSerializer(course, many=True)
        return Response(serializer.data)

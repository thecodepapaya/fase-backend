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
from faculty.models import Faculty


class course_list(APIView):
    def get(self, request, format=None):
        course = Course.objects.filter(start_timestamp__gte=timezone.now(
        )-timedelta(minutes=30)).filter(start_timestamp__lte=timezone.now())
        serializer = CourseSerializer(course, many=True)
        return Response(serializer.data)


class course_detail(APIView):
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        course = self.get_object(pk)
        received_access_token = request.GET.get('token','-')
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            stored_access_token = Faculty.objects.get(
                institute_email=request.data['instructor'].institute_email).access_token
            if received_access_token != stored_access_token:
                return Response({'detail': 'Invalid access token, try logging out and logging in again'}, status=status.HTTP_401_UNAUTHORIZED)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

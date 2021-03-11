import logging

from course.models import Course
from course.serializers import CourseSerializer
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Faculty
from .serializers import FacultySerializer

logger = logging.getLogger(__file__)


class faculty_list(APIView):
    def get(self, request, format=None):
        faculty = Faculty.objects.all()
        serializer = FacultySerializer(faculty, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        logger.info(f"POST request body: {request.data}")
        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid():
            faculty = Faculty.objects.filter(
                institute_email=serializer.validated_data['institute_email'])
            if faculty.exists():
                logger.info(f"Registration for existing faculty {request.data}")
                new_fac = faculty[0]
                new_fac.access_token = request.data['access_token']
                new_fac.name = request.data['name']
                new_fac.google_uid = request.data['google_uid']
                new_fac.save()
                return Response({'access_token': new_fac.access_token}, status=status.HTTP_201_CREATED)
            else:
                logger.info(f"Registration for new faculty {request.data}")
                serializer.save()
                return Response({'access_token': request.data['access_token']}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class faculty_course(APIView):
    def get(self, request, email, format=None):
        received_access_token = request.GET.get('token', '-')
        try:
            faculty = Faculty.objects.get(institute_email=email)
            stored_access_token = faculty.access_token
            if received_access_token != stored_access_token:
                logger.warn(f"Access token invaid. Received token: {received_access_token} Stored token: {stored_access_token}")
                return Response({'detail': 'Invalid access token, try logging out and logging in again'}, status=status.HTTP_401_UNAUTHORIZED)
        except Faculty.DoesNotExist:
            logger.error(f"Cannot find faculty with email {email}")
            return Response({'detail': f'Faculty with email {email} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        courses = Course.objects.filter(instructor=faculty)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

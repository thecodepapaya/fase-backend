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
        logger.info(f"GET faculty_list request data: {request.data}")
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
                logger.info(
                    f"Registration for existing faculty {request.data}")
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
        logger.info(f"GET faculty_course request data: {request.data}")
        received_access_token = request.GET.get('token', '-')
        try:
            faculty = Faculty.objects.get(institute_email=email)
            stored_access_token = faculty.access_token
            if received_access_token != stored_access_token:
                logger.warn(
                    f"Access token invaid. Received token: {received_access_token} Stored token: {stored_access_token}")
                return Response({'detail': 'Invalid access token, try logging out and logging in again'}, status=status.HTTP_401_UNAUTHORIZED)
        except Faculty.DoesNotExist:
            logger.error(f"Cannot find faculty with email {email}")
            return Response({'detail': f'Faculty with email {email} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        courses = Course.objects.filter(instructor=faculty)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class faculty_verify(APIView):
    def get(self, request, format=None):
        logger.info(f"Verification for faculty_verify")
        received_access_token = request.GET.get('token', '-')
        received_google_uid = request.GET.get('uid', '-')
        received_institute_email = request.GET.get('email', '-')
        try:
            faculty = Faculty.objects.get(
                institute_email=received_institute_email)
        except Faculty.DoesNotExist:
            logger.warn(
                f"Cannot find faculty with email {received_institute_email}, registration verification failed")
            return Response({'detail': f'Could\'nt find faculty with email {received_institute_email}'}, status=status.HTTP_404_NOT_FOUND)
        if faculty.google_uid == received_google_uid and faculty.access_token == received_access_token:
            logger.info(f"Verified OK Registration for faculty {received_institute_email}")
            return Response(status=status.HTTP_200_OK)
        else:
            logger.warn(
                f"Failed faculty verification attempt")
            logger.info(
                f"Received Email: {received_institute_email} Google UID: {received_google_uid} Access Token: {received_access_token}")
            logger.info(
                f"Stored Email: {faculty.institute_email} Google UID: {faculty.google_uid} Access Token: {faculty.access_token}")
            return Response({'detail': 'Verification failed. Credentials do not match'}, status=status.HTTP_401_UNAUTHORIZED)

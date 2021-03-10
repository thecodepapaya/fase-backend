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


class faculty_list(APIView):
    # def get(self, request, format=None):
    #     faculty = Faculty.objects.all()
    #     serializer = FacultySerializer(faculty, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class faculty_course(APIView):
    def get(self, request, email, format=None):
        try:
            faculty = Faculty.objects.get(institute_email=email)
            stored_access_token = faculty.access_token
            # TODO: Check access token of faculty before sending courses, use query parameters
            received_access_token = request.GET.get('token', '-')
            if received_access_token != stored_access_token:
                return Response({'detail': 'Invalid access token, try logging out and logging in again'}, status=status.HTTP_401_UNAUTHORIZED)
        except Faculty.DoesNotExist:
            return Response({'detail': f'Faculty with email {email} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        courses = Course.objects.filter(instructor=faculty)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

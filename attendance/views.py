from datetime import timedelta

from course.models import Course
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from meta.models import MetaData
from meta.serializers import MetaDataSerializer
from registration.models import Registration
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Attendance
from .serializers import AttendanceSerializer


class attendance_list(APIView):
    def get(self, request, format=None):
        attendance = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['student_data'].institute_email
            meta_data = MetaData.objects.all()[0]
            registration_data = Registration.objects.filter(
                student_data__institute_email=email)[0]
            if serializer.validated_data['app_build_number'] < meta_data.min_app_build:
                return Response(MetaDataSerializer(meta_data).data, status=status.HTTP_403_FORBIDDEN)
            # If registration was invalidated or server_key is not correct
            if serializer.validated_data['server_key'] != registration_data.server_key:
                return Response({'detail': 'Your registeration has been invalidated, register again'}, status=status.HTTP_403_FORBIDDEN)
            # Check if the attendance is within the time frame
            course = Course.objects.get(
                course_code=serializer.validated_data['course'].course_code)
            if course.start_timestamp > timezone.now():
                return Response({'detail': 'Attendance window has not started yet'}, status=status.HTTP_403_FORBIDDEN)
            if (course.start_timestamp + timedelta(minutes=30) <= timezone.now()):
                return Response({'detail': 'Time limit to mark attendance expired'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class my_attendance(APIView):
    def get(self, request, email, course, format=None):
        email = email+'@iiitvadodara.ac.in'
        print(f"email: {email}")
        print(f"course: {course}")
        attendances_record = Attendance.objects.filter(
            student_data__institute_email=email).filter(course__course_code=course)
        return Response({'count': len(attendances_record)}, status=status.HTTP_200_OK)

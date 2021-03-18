import logging
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
from students.models import StudentData

logger = logging.getLogger(__file__)


class attendance_list(APIView):
    def get(self, request, format=None):
        attendance = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        logger.info(f"POST request body: {request.data}")
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['student_data'].institute_email
            meta_data = MetaData.objects.all()[0]
            registration_data = Registration.objects.filter(
                student_data__institute_email=email)[0]
            if serializer.validated_data['app_build_number'] < meta_data.min_app_build:
                logger.warn(
                    f"App build number({serializer.validated_data['app_build_number']}) less than allowed build number({meta_data.min_app_build})")
                return Response(MetaDataSerializer(meta_data).data, status=status.HTTP_403_FORBIDDEN)
            # If registration was invalidated or server_key is not correct
            if serializer.validated_data['server_key'] != registration_data.server_key:
                logger.warn(
                    f"Server key mismatch. Received server_key: {serializer.validated_data['server_key']} Stored server_key: {registration_data.server_key}")
                return Response({'detail': 'Your registeration has been invalidated, register again'}, status=status.HTTP_403_FORBIDDEN)
            # Check if the attendance is within the time frame
            course = Course.objects.get(
                course_code=serializer.validated_data['course'].course_code)
            if course.start_timestamp > timezone.now():
                logger.warn(
                    f"Attempt to mark attendance before attendance window opens. Email: {email} Course: {course}")
                return Response({'detail': 'Attendance window has not started yet'}, status=status.HTTP_403_FORBIDDEN)
            if (course.start_timestamp + timedelta(minutes=30) <= timezone.now()):
                logger.warn(
                    f"Attempt to mark attendance after attendance window closed. Email: {email} Course: {course}")
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


class attendance_ble_count(APIView):
    def post(self, request, format=None):
        logger.info(f"POST attendance_ble_count request data {request.data}")
        received_server_key = request.GET.get('key', '-')
        received_ble_count = request.GET.get('ble', '0')
        received_attendance_id = request.GET.get('id', '-')
        if int(received_ble_count) < 0:
            logger.error(
                f"BLE count invalid for attendance {received_attendance_id} and server_key {received_server_key}, BLE count must be >=0. Received BLE count was {received_ble_count}")
            return Response({'detail': 'Invalid BLE count received'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            stored_attendance = Attendance.objects.get(
                attendance_id=received_attendance_id)
            if received_server_key != stored_attendance.server_key:
                logger.error(
                    f"Server key mismatch. Received server_key: {received_server_key} Stored server key: {stored_attendance.server_key}")
                return Response({'detail': f'Server key invalid for attendance id {received_attendance_id}'}, status=status.HTTP_401_UNAUTHORIZED)
            stored_attendance.ble_verifications_count = received_ble_count
            stored_attendance.save()
            return Response(status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            logger.error(
                f"Could not find attendance for received attendance id {received_attendance_id}")
            return Response({'detail': f'Could not find attendance with id {received_attendance_id}'}, status=status.HTTP_404_NOT_FOUND)

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
from students.models import StudentData

from attendance.models import Attendance, BleVerification
from attendance.serializers import (AttendanceSerializer,
                                    BleVerificationSerializer)

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
            if (course.start_timestamp + timedelta(minutes=course.attendance_duration) <= timezone.now()):
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


class ble_verification(APIView):

    # TODO: remove later
    def get(self, request, format=None):
        ble_verification = BleVerification.objects.all()
        serializer = BleVerificationSerializer(ble_verification, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        logger.info(f"POST ble_verification request data {request.data}")
        received_server_key = request.GET.get('key', '-')
        serializer = BleVerificationSerializer(data=request.data)
        if serializer.is_valid():
            if BleVerification.objects.filter(
                    verified_by=serializer.validated_data['verified_by'], verified_for=serializer.validated_data['verified_for']).exists():
                logger.error(
                    f'Duplicate verification for attendance ID {serializer.validated_data["verified_for"]} by {serializer.validated_data["verified_by"]}')
                return Response({'detail': f'Attendance for ID {serializer.validated_data["verified_for"]} already verified by {serializer.validated_data["verified_by"]}'}, status=status.HTTP_208_ALREADY_REPORTED)
            try:
                verified_by = Registration.objects.filter(
                    student_data__institute_email=serializer.validated_data['verified_by'])[0]
            except Registration.DoesNotExist:
                logger.error(
                    f"Failed to fetch student with email {serializer.validated_data['verified_by']}, not found")
                return Response({'detail': f'Could not find record of student with email {serializer.validated_data["verified_by"]}, attendance not verified'}, status=status.HTTP_404_NOT_FOUND)
            if not Attendance.objects.filter(attendance_id=serializer.validated_data['verified_for']).exists():
                logger.error(
                    f"Failed to fetch attendance with id {serializer.validated_data['verified_for']}, not found")
                return Response({'detail': f'Could not find record of attenace with id {serializer.validated_data["verified_for"]}, attendance not verified'}, status=status.HTTP_404_NOT_FOUND)
            if verified_by.server_key != received_server_key:
                logger.error(
                    f"Server key invalid for BLE attendance verification. Received server key {received_server_key} stored server_key {verified_by.server_key}")
                return Response({'detail': 'Server key mismatch. You are not allowed to authenticate attendances. Try registering again'}, status=status.HTTP_401_UNAUTHORIZED)

            serializer.save()
            logger.info(
                f"Verified attendance for ID {serializer.validated_data['verified_for']} by {serializer.validated_data['verified_by']}")
            return Response(status=status.HTTP_200_OK)
        else:
            logger.error(f"BAD POST request ble_verification {request.data}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

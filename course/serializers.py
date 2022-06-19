import logging
from datetime import datetime, timedelta

from attendance.models import Attendance
from django.http import Http404
from rest_framework import serializers
from users.serializers import UserSerializer

from course.models import Course, CourseWindowRecord
from attendance.models import Attendance

logger = logging.getLogger(__file__)


class CourseSerializer(serializers.ModelSerializer):
    instructors = UserSerializer(many=True, read_only=True)
    is_already_marked = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id',
            'course_code',
            'course_name',
            'section',
            'semester',
            'academic_year',
            'instructors',
            'start_timestamp',
            'attendance_duration_in_minutes',
            'is_already_marked',
            'color',
        )

    def get_is_already_marked(self, course):
        user = self.context.get('request').user
        logger.info(f'User: {user}')

        if not course.start_timestamp:
            return False

        attendance_window_start = course.start_timestamp
        attendance_window_end = course.start_timestamp + \
            timedelta(minutes=course.attendance_duration_in_minutes)

        attendance = Attendance.objects.filter(
            student=user, course=course, timestamp__gte=attendance_window_start, timestamp__lte=attendance_window_end).exists()

        if not attendance:
            return False

        return True

    def get_color(self, course):
        user = self.context.get('request').user
        logger.info(f'User: {user}')

        red = "#dc3545"
        yellow = "#ffc107"
        green = "#198754"

        try:
            marked_attendance_count = Attendance.objects.filter(
                course=course, student=user).count()

            total_attendance_count = CourseWindowRecord.objects.filter(
                course=course).count()

            percentage = (marked_attendance_count/total_attendance_count)*100

        except Exception as e:
            logger.warning(f'Error {e} calculating attendance percentage. Defaulting to 100.')
            percentage = 100

        color = None

        if percentage <= 75:
            color = red
        elif 75 < percentage <= 80:
            color = yellow
        else:
            color = green

        return color

    def create(self, validated_data):
        user = self.context['request'].user

        if 'instructors' in validated_data:
            _ = validated_data.pop('instructors')

        course = Course.objects.create(**validated_data)

        course.instructors.add(user.institute_email)

        return course

    # TODO move into signals
    def update(self, instance, validated_data):

        validated_start_timestamp = validated_data.get(
            'start_timestamp', instance.start_timestamp)
        instance_start_timestamp = instance.start_timestamp
        has_attendance_started = instance_start_timestamp != validated_start_timestamp

        logger.info(f'Has attendance started: {has_attendance_started}')

        instance.course_name = validated_data.get(
            'course_name', instance.course_name)
        instance.course_code = validated_data.get(
            'course_code', instance.course_code)
        instance.section = validated_data.get(
            'section', instance.section)
        instance.semester = validated_data.get('semester', instance.semester)
        instance.academic_year = validated_data.get(
            'academic_year', instance.academic_year)
        instance.start_timestamp = validated_data.get(
            'start_timestamp', instance.start_timestamp)
        instance.attendance_duration_in_minutes = validated_data.get(
            'attendance_duration_in_minutes', instance.attendance_duration_in_minutes)

        instance.save()

        # Check and create a record of CourseWindowRecord if start_timestamp of the course has changed
        if(has_attendance_started):
            course_window_record = CourseWindowRecord(
                course_id=instance.id,
                start_timestamp=instance.start_timestamp,
                attendance_duration_in_minutes=instance.attendance_duration_in_minutes,)

            course_window_record.save()

        return instance

import logging
from datetime import datetime
from os import stat
from httplib2 import Response

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions

from .models import Course, CourseWindowRecord
from .serializers import CourseSerializer

logger = logging.getLogger(__file__)


class CourseViewset(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        is_faculty = user.groups.filter(name='Faculty').exists()

        logger.info(f'CourseViewset.get_queryset is_faculty: {is_faculty}')
        logger.info(f'CourseViewset.get_queryset user: {user}')

        if is_faculty:
            courses = Course.objects.filter(
                instructors__institute_email=user.institute_email, is_active=True)
        else:
            courses = Course.objects.filter(
                students__institute_email=user.institute_email, is_active=True)

        return courses

    # @action(methods=['get'], detail=False, url_path="((?P<course_id>[^/.]+))/start")
    # def start_attendance(self, request, course_id):
    #     user = request.user
    #     print('course_id')
    #     print(course_id)

    #     now = datetime.now()

    #     try:

    #         course = Course.objects.get(id=course_id)
    #         course.start_timestamp = now
    #         course.save()

    #         duration = course.attendance_duration_in_minutes

    #         CourseWindowRecord.objects.create(
    #             course_id=course_id, start_timestamp=now, attendance_duration_in_minutes=duration,)

    #     except Course.DoesNotExists:
    #         return Response(status=404)

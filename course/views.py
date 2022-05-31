import logging

from rest_framework import viewsets

from .models import Course
from .serializers import CourseSerializer

logger = logging.getLogger(__file__)


class CourseViewset(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        is_faculty = user.groups.filter(name='Faculty').exists()

        logger.info(f'CourseViewset.get_queryset is_faculty: {is_faculty}')
        logger.info(f'CourseViewset.get_queryset user: {user}')

        if is_faculty:
            courses = Course.objects.filter(
                instructors__institute_email=user.institute_email)
        else:
            courses = Course.objects.filter(
                students__institute_email=user.institute_email)

        return courses

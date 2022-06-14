import logging

from rest_framework import viewsets

from .models import Course
from .serializers import CourseSerializer

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from users.models import User
import pandas as pd

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
                instructors__institute_email=user.institute_email, is_active=True)
        else:
            courses = Course.objects.filter(
                students__institute_email=user.institute_email, is_active=True)

        return courses


# TODO needs a refactor :time_bomb:
@api_view(http_method_names=['POST', ])
@permission_classes((permissions.AllowAny,))
def bulk_register_students(request):

    user = request.user
    # print(user)
    course_code = request.data['course_code']
    section = request.data['section']
    is_faculty = user.groups.filter(name='Faculty').exists()

    if is_faculty:

        course = Course.objects.get(course_code=course_code, section=section)
        csv = request.FILES['file']
        df = pd.read_csv(csv)
        for i in df.index:
            user_obj, _ = User.objects.get_or_create(
                institute_email=str(df['rollno'][i])+"@iiitvadodara.ac.in",
                name=df['name'][i]
            )
            # print(user_obj)
            user_obj.save()
            course.students.add(user_obj)

        course.save()

        return Response({"message": f"Successful enrolled students in {course_code}"})

    else:
        return Response(status=403)

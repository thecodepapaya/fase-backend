import logging

from course.models import Course, CourseWindowRecord
from django.http import HttpResponse
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from .generate_spreadsheet import generate_workbook_for_single_course
from .models import Attendance
from .serializers import AttendanceSerializer

logger = logging.getLogger(__file__)


class AttendanceViewset(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        query_set = Attendance.objects.filter(student=user)

        return query_set


@api_view(http_method_names=['GET', ])
# @permission_classes((permissions.IsAuthenticated,)) # TODO uncomment
@permission_classes((permissions.AllowAny,))
def generate(request, course_id):
    try:
        course = Course.objects.get(id=course_id)

        file_path = generate_workbook_for_single_course(course)

        try:
            with open(file_path, 'rb') as excel:
                file_data = excel.read()

            # sending response
            response = HttpResponse(file_data)
            response['Content-Disposition'] = f'attachment; filename="{course.course_code}-attendance.xlsx"'
            response['Content-Length'] = len(file_data)
            response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        except IOError:
            response = Response(status=404)

        return response

    except Course.DoesNotExist:
        return Response(status=404)

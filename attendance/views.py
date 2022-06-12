import logging

from django.http import HttpResponseNotFound, HttpResponse

from course.models import Course, CourseWindowRecord
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .generate_spreadsheet import generate_workbook_for_single_course
from .models import Attendance
from .serializers import AttendanceSerializer

logger = logging.getLogger(__file__)


class AttendanceViewset(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


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

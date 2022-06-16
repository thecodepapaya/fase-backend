import logging

import pandas as pd
from django.contrib import messages
from authentication.views import assign_user_group
from users.models import User

from ..models import Course

logger = logging.getLogger(__file__)


def add_students_from_csv(course: Course, request):

    csv = course.course_student_mapper_file

    if not csv:
        messages.warning(
            request, f'No CSV found, please add a CSV to course ID {course.id}. Aborting import.')

        logger.warning('No CSV found, aborting import')
        return

    try:
        course.students.clear()
        student_data = pd.read_csv(csv)

        for index in student_data.index:

            institute_email = student_data['email'][index]
            name = student_data['name'][index]

            user_obj, is_created = User.objects.get_or_create(
                institute_email=institute_email, name=name)
            
            if is_created:
                assign_user_group(user_obj)
            
            course.students.add(user_obj)

        course.save()

        messages.info(
            request, f'Successfully populated student list from CSV for course ID {course.id}')

        return

    except Exception as e:
        messages.error(
            request, f'Error occurred. Please check if the CSV is properly formatted. Error {e}. Aborting import for course ID {course.id}')

        logger.warning(f'Failed to add students to course: {e}')
        return

import logging
import os
from datetime import timedelta

from course.models import Course, CourseWindowRecord
from users.models import User
from xlsxwriter import Workbook, worksheet

from attendance.models import Attendance

logger = logging.getLogger(__file__)


_date_format = None
_date_time_format_string = 'dd/mm/yy - hh:mm'
_date_time_format_data = {
    'num_format': _date_time_format_string, 'align': 'left'}


def generate_workbook_for_single_course(course: Course):
    workbook, file_path = _create_attendance_workbook(course.course_code)
    worksheet = workbook.add_worksheet(name=course.course_code)

    _populate_worksheet_for_course(course, worksheet)

    workbook.close()

    return file_path


# TODO create this method for all attendances
# def generate_workbook_for_all_courses(user:User):
def generate_workbook_for_all_courses():
    workbook, file_path = _create_attendance_workbook('all_attendance')
    # courses = Course.objects.filter(instructor.)
    worksheet = workbook.add_worksheet(name='course.course_code')

    return worksheet


def _create_attendance_workbook(name='attendance'):
    dir_path = '/tmp/generated_attendances/'

    path_exists = os.path.exists(dir_path)

    if not path_exists:
        os.mkdir(dir_path)

    file_path = f'{dir_path}{name}.xlsx'
    workbook = Workbook(file_path, {'remove_timezone': True})

    global _date_format
    _date_format = workbook.add_format(_date_time_format_data)

    return workbook, file_path


def _populate_worksheet_for_course(course: Course, worksheet: worksheet):

    attendance_windows = CourseWindowRecord.objects.filter(course=course)
    students = course.students.all()

    _populate_student_names_and_attendance_columns(
        students, attendance_windows, worksheet)

    row = 1
    column = 1
    for window in attendance_windows:
        marked_attendances = _get_marked_attendances_for_window(window)
        row = 1

        for student in students:
            has_marked = marked_attendances.filter(student=student).exists()
            worksheet.write(row, column, has_marked)
            row += 1

        column += 1

    return worksheet


def _get_marked_attendances_for_window(attendance_window: CourseWindowRecord):

    course = attendance_window.course

    window_start_time = attendance_window.start_timestamp
    window_close_time = window_start_time + \
        timedelta(minutes=attendance_window.attendance_duration_in_minutes)

    marked_attendances = Attendance.objects.filter(
        course=course, timestamp__gte=window_start_time, timestamp__lte=window_close_time)

    return marked_attendances


def _populate_student_names_and_attendance_columns(students, attendance_windows, worksheet):
    worksheet.write(0, 0, 'Students/Attendance')

    row = 1
    column = 1

    for student in students:
        worksheet.write(row, 0, student.institute_email)
        row += 1

    for window in attendance_windows:
        indian_time = window.start_timestamp + \
            timedelta(hours=5.5)  # UTC to indian time
        worksheet.write_datetime(0, column, indian_time, _date_format)
        column += 1

    worksheet.set_column(0, 0, 35)

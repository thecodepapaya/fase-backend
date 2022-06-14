
import logging

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import pandas as pd
from users.models import User

from .models import Course, CourseWindowRecord

logger = logging.getLogger(__file__)


@receiver(pre_save, sender=Course)
def create_attendance_record(sender, instance, *args, **kwargs):
    # print('pre_save')
    # logger.warning('pre_save')
    pass


@receiver(post_save, sender=Course)
def populate_students_from_csv(sender, instance: Course, created, **kwargs):
    # csv = instance.
    # print('post_save')
    # logger.warning('post_save')
    course_id = instance.id
    course = Course.objects.get(id=course_id)

    existing_students = course.students.all()
    existing_students_set = set(existing_students)

    csv = instance.course_student_mapper_file
    student_data = pd.read_csv(csv)

    for index in student_data.index:

        institute_email = student_data['email'][index]
        name = student_data['name'][index]

        user_obj, _ = User.objects.get_or_create(
            institute_email=institute_email, name=name)

        print(user_obj)

        course.students.add(user_obj)

    updated_students = course.students.all()
    updated_students_set = set(updated_students)

    intersection_set = existing_students_set.intersection(updated_students_set)
    should_update_course_model = len(intersection_set) != 0

    print('===================')
    print(should_update_course_model)
    print(existing_students)
    print(updated_students)

    if should_update_course_model:
        print('Updating course model')
        course.students.clear()
        print('Cleared Students')
        course.students.add(updated_students)
        print('Updated students')
        course.save()
        print('Saved! Yay')


@receiver(post_save, sender=Course)
def other_post_save_actions(sender, instance, created, **kwargs):
    # print('pre_save_2')
    # logger.warning('post_save_2')

    # perform a different kind of post save action here
    pass

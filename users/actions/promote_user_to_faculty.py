import logging

from django.contrib import messages
from django.contrib.auth.models import Group
from users.models import User

logger = logging.getLogger(__file__)


def promote_user_to_faculty(user: User, request):
    group_name = 'Faculty'

    try:
        faculty_group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        messages.warning(
            request, f'Group \'{group_name}\' does not exists. Please create a group \'{group_name}\' with appropriate permissions in the admin panel')
        return

    try:

        user.groups.clear()
        user.groups.add(faculty_group)
        user.set_password('1234')
        user.is_staff = True
        user.save()
        messages.info(
            request, f'Upgraded {user} to role \'{faculty_group.name}\'.')
    except Exception as e:
        messages.error(
            request, f'Failed to upgrade role for {user}. Error {e}.')

import logging

from django.contrib.auth.models import Group
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer

from authentication.firebase import decode_token

logger = logging.getLogger(__file__)


@permission_classes([permissions.AllowAny])
@api_view(http_method_names=['POST', ])
def login(request):
    token_header = request.headers.get('Authorization')

    if not token_header:
        return Response(status=401)

    jwt_token = token_header.split(' ')[1]
    decoded_token = decode_token(jwt_token)

    if not decoded_token:
        return Response(status=401)

    email = decoded_token.get('email')
    name = decoded_token.get('name')
    picture = decoded_token.get('picture', None)

    user, is_created = User.objects.get_or_create(
        pk=email, defaults={'name': name, 'display_picture': picture})

    if is_created:
        response_code = 201
        _assign_user_group(user)
    else:
        response_code = 200

    serializer = UserSerializer(user)

    return Response(data=serializer.data, status=response_code)


def _get_group(email):
    faculty_group = Group.objects.get(name='Faculty')
    student_group = Group.objects.get(name='Student')

    is_student = email.split('@')[0].startswith('20')

    group = student_group if is_student else faculty_group

    logger.info(f'Selected Group for new user: {group}')

    return group


def _assign_user_group(user):
    already_has_group = user.groups.count() != 0

    if already_has_group:
        logger.info(f'{user} already has groups {user.groups}, returning')
        return

    group = _get_group(user.pk)
    user.groups.add(group)

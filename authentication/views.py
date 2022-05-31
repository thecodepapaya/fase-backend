import token
import jwt
from rest_framework import viewsets

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions

from authentication.firebase import decode_token
from .permissions import SkipAuth
from users.models import User
from users.serializers import UserSerializer


@permission_classes([SkipAuth])
@api_view(http_method_names=['POST', ])
def login(request):
    token_header = request.headers.get('Authorization')

    if not token_header:
        return Response(status=401)

    jwt_token = token_header.split(' ')[1]
    decoded_token = decode_token(jwt_token)

    if not decoded_token:
        return Response(status=401)

    user, response_code = _get_or_create_user(decoded_token)
    serializer = UserSerializer(user)

    return Response(data=serializer.data, status=response_code)


def _get_or_create_user(decoded_token):
    email = decoded_token.get('email')
    name = decoded_token.get('name')
    picture = decoded_token.get('picture', None)
    response_code = 200

    try:
        user = User.objects.get(pk=email)
        print(f'Get user: {user}')
    except User.DoesNotExist:
        user = _create_user(email, name, picture)
        print(f'New user: {user}')
        response_code = 201

    return user, response_code


def _create_user(email, name, picture):
    user = User(institute_email=email, name=name, display_picture=picture)
    user.save()

    return user

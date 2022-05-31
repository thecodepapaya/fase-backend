from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer

from authentication.firebase import decode_token


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
    response_code = 201 if is_created else 200

    serializer = UserSerializer(user)

    return Response(data=serializer.data, status=response_code)

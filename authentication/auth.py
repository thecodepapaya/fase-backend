from django.contrib.auth.backends import BaseBackend
from .firebase import get_email_from_token
from users.models import User
from rest_framework import authentication

import logging
import traceback

logger = logging.getLogger(__file__)


class FirebaseJwtBackend(authentication.BaseAuthentication):

    def authenticate(self, request):
        bearer_token = request.headers.get('Authorization')
        if not bearer_token:
            return None

        jwt_token = bearer_token.split(' ')[1]

        if not jwt_token:
            return None

        try:
            email = get_email_from_token(jwt_token)
            user = User.objects.get(pk=email)
            return (user, None)

        except Exception as e:
            logging.error(traceback.format_exc())
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user

        except User.DoesNotExists:
            return None

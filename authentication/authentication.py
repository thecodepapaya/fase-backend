from django.contrib.auth.backends import BaseBackend
from firebase import get_email_from_token
from users import User


class FirebaseJwtBackend(BaseBackend):

    def authenticate(self, request, token=None):
        email = get_email_from_token(token)

        try:
            user = User.objects.filter(institute_email=email)
            return user

        except User.DoesNotExists:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.filter(institute_email=user_id)
            return user

        except User.DoesNotExists:
            return None

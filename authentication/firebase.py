import logging

import firebase_admin
from firebase_admin import auth, credentials

logger = logging.getLogger(__file__)


cred = credentials.Certificate(
    "fase-35702-firebase-adminsdk-hh8di-558e6de6c5.json")
firebase_admin.initialize_app(cred)


def decode_token(id_token):
    decoded_token = auth.verify_id_token(id_token)

    return decoded_token


def get_email_from_token(id_token):
    decoded_token = decode_token(id_token)

    email = decoded_token.get('email')
    logger.info(f'Email from JWT: {email}')

    return email

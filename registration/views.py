import json
import logging

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Registration
from .serializers import RegistrationSerializer
from .utils import send_mail
from fase_backend import settings

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__file__)


class RegistrationViewset(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['post'], detail=False, url_path="verify")
    def verify_registration(self, request):
        user = request.user
        device_id = request.data.get('device_id', None)

        if not device_id:
            return Response(data={'message': 'device_id is required'}, status=400)

        registration = Registration.objects.filter(device_id=device_id).first()

        if not registration:
            return Response(data={'message': 'Registration not found'}, status=404)

        registration_valid = registration.student == user

        if registration_valid:
            serializer = RegistrationSerializer(registration)
            return Response(data=serializer.data, status=200)
        else:
            scheduler = BackgroundScheduler()
            scheduler.add_job(func = mails, args = (user.name, user.institute_email[:user.institute.index("@")], device_id, registration.device_id))
            scheduler.start()
            return Response(data={'message': 'Registration invalid, please register again'}, status=404)


def mails(name, rollno, new_device, old_device):

    params = {"name": name, "rollno": rollno, "new_device": new_device, "old_device": old_device}

    send_mail(params, settings.EMAIL, settings.PASSWORD)

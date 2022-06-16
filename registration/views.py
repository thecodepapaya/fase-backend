import json
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from fase_backend import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions

from .models import Registration
from .serializers import RegistrationSerializer
from .utils import send_mail

logger = logging.getLogger(__file__)


class RegistrationViewset(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        user = self.request.user
        query_set = Registration.objects.filter(student=user)

        return query_set

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
            # TODO refactor to reduce cognitive complexity
            scheduler = BackgroundScheduler()
            scheduler.add_job(func=mails, args=(user.name, user.institute_email[:user.institute_email.index(
                "@")], device_id, registration.device_id))
            scheduler.start()
            return Response(data={'message': 'Registration invalid, please register again'}, status=404)


# TODO avoid the assumption that email has the format <roll_number@iiitvadodara.ac.in>
def mails(name, rollno, new_device, old_device):

    params = {"name": name, "rollno": rollno,
              "new_device": new_device, "old_device": old_device}

    send_mail(params, settings.EMAIL, settings.PASSWORD)

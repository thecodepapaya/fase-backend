
import logging
from datetime import datetime
from hashlib import sha1

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from meta.models import MetaData
from meta.serializers import MetaDataSerializer
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Registration
from .serializers import RegistrationSerializer

logger = logging.getLogger(__file__)


class registration_list(APIView):
    def get(self, request, format=None):
        registration = Registration.objects.all()
        serializer = RegistrationSerializer(registration, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        logger.info(f"POST request body: {request.body}")
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            meta_data = MetaData.objects.all()[0]
            if serializer.validated_data['app_build_number'] < meta_data.min_app_build:
                logger.warn(f"App build number({serializer.validated_data['app_build_number']}) less than allowed build number({meta_data.min_app_build})")
                return Response(MetaDataSerializer(meta_data).data, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class registration_detail(APIView):
    def get_object(self, pk):
        try:
            return Registration.objects.get(pk=pk)
        except Registration.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        registration = self.get_object(pk)
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        registration = self.get_object(pk)
        serializer = RegistrationSerializer(registration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        registration = self.get_object(pk)
        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class registration_verification(APIView):

    def post(self, request, format=None):
        logger.info(f"POST request body: {request.body}")
        try:
            email = request.data['institute_email']
            server_key = request.data['server_key']
            registration_data = Registration.objects.filter(
                student_data__institute_email=email)
            if len(registration_data) == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if server_key != registration_data[0].server_key:
                logger.warn(f"Server key mismatch. Received server_key: {server_key} Stored server_key: {registration_data[0].server_key}")
                return Response(status=status.HTTP_403_FORBIDDEN)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

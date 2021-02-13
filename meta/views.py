
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MetaData
from .serializers import MetaDataSerializer


class metadata_latest(APIView):
    def get(self, request, format=None):
        meta_data = MetaData.objects.all()[0]
        serializer = MetaDataSerializer(meta_data)
        return Response(serializer.data)

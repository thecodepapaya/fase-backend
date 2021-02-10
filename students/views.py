from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import StudentData
from .serializers import StudentDataSerializer


class students_list(APIView):
    def get(self, request, format=None):
        student_data = StudentData.objects.all()
        serializer = StudentDataSerializer(student_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class students_detail(APIView):
    def get_object(self, pk):
        try:
            return StudentData.objects.get(pk=pk)
        except StudentData.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student_data = self.get_object(pk)
        serializer = StudentDataSerializer(student_data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        student_data = self.get_object(pk)
        serializer = StudentDataSerializer(student_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        student_data = self.get_object(pk)
        student_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

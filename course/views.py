from unicodedata import name
from django.shortcuts import render

from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer


class CourseViewset(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        is_faculty = user.groups.filter(name='Faculty').exists()

        if is_faculty:
            courses = Course.objects.filter(
                instructors__institute_email=user.institute_email)
        else:
            courses = Course.objects.filter(
                students__institute_email=user.institute_email)
                
        return courses

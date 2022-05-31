from django import views
from rest_framework import routers
from course.views import CourseViewset
from users.views import UserViewset
from meta.views import MetadataViewset
from registration.views import RegistrationViewset
from attendance.views import AttendanceViewset

router = routers.DefaultRouter()

router.register(r'courses', CourseViewset, basename='courses')
router.register(r'users', UserViewset)
router.register(r'metadata', MetadataViewset, basename='metadata')
router.register(r'registration', RegistrationViewset, basename='registration')
router.register(r'attendance', AttendanceViewset, basename='attendance')

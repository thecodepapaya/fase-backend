from rest_framework import routers
from course.views import CourseViewset

router = routers.DefaultRouter()

router.register(r'courses', CourseViewset)

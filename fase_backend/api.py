from rest_framework import routers
from course.views import CourseViewset
from users.views import UserViewset

router = routers.DefaultRouter()

router.register(r'courses', CourseViewset,basename='courses')
router.register(r'users', UserViewset)

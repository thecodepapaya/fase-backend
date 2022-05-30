from rest_framework import routers
from course.views import CourseViewset
from users.views import UserViewset
# from authentication.views import TokenViewset
from meta.views import MetadataViewset

router = routers.DefaultRouter()

router.register(r'courses', CourseViewset, basename='courses')
router.register(r'users', UserViewset)
# router.register(r'login', TokenViewset, basename='login')
router.register(r'metadata', MetadataViewset, basename='metadata')

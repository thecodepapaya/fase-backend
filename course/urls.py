from rest_framework import routers
from course import views as myapp_views

router = routers.DefaultRouter()
router.register(r'courses', myapp_views.CourseViewset)

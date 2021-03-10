from django.urls import path
from faculty import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('faculty/', views.faculty_list.as_view()),
    # path('faculty/email/', views.faculty_course.as_view()),
    path('faculty/<email>/', views.faculty_course.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

from django.urls import path
from course import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('course/', views.course_list.as_view()),
    path('course/<slug:pk>/', views.course_detail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

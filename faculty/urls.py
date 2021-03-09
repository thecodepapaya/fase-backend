from django.urls import path
from faculty import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('faculty/', views.faculty_list.as_view()),
    # path('course/<int:pk>/', views.course_detail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

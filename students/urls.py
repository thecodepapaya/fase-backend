from django.urls import path
from students import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('students/', views.students_list.as_view()),
    path('students/<int:pk>/', views.students_detail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

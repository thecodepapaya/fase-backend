from django.urls import path
from registration import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('registration/', views.registration_list.as_view()),
    path('registration/<int:pk>/', views.registration_detail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

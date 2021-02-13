from django.urls import path
from meta import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('meta/', views.metadata_latest.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

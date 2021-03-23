from django.urls import path
from attendance import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('attendance/', views.attendance_list.as_view()),
    # path('attendance/<int:pk>/', views.attendance_detail.as_view()),
    path('attendance/<slug:email>/<slug:course>/', views.my_attendance.as_view()),
    path('ble-verification/', views.ble_verification.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)

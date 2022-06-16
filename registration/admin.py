from django.contrib import admin
from django.http import HttpRequest

from registration.models import Registration


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'student', 'timestamp')
    search_fields = ['id', 'student__name',
                     'student__institute_email', 'device_id']
    raw_id_fields = ('student',)

    def get_queryset(self, request: HttpRequest):
        user = request.user
        query_set = super().get_queryset(request)

        is_student = user.groups.filter(name="Student").exists()

        if is_student:
            filtered_query_set = query_set.filter(student=user)

        # All registrations for faculty and admins
        else:
            filtered_query_set = query_set

        return filtered_query_set


admin.site.register(Registration, RegistrationAdmin)

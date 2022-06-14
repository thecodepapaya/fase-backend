from django.contrib import admin

from registration.models import Registration


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'student', 'timestamp')
    search_fields = ['id','student__name', 'student__institute_email', 'device_id']


admin.site.register(Registration, RegistrationAdmin)

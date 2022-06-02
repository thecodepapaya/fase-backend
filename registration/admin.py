from django.contrib import admin

from registration.models import Registration

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'student', 'timestamp')


admin.site.register(Registration, RegistrationAdmin)

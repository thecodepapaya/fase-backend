from django.contrib import admin

from registration.models import Registration

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'student', 'timestamp')
    search_fields = ['student', 'device_id']


admin.site.register(Registration, RegistrationAdmin)

from django.contrib import admin

from registration.models import Registration, RegistrationAdmin

admin.site.register(Registration, RegistrationAdmin)

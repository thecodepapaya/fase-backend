from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('institute_email', 'name', 'is_faculty')
    search_fields = ['name', 'institute_email', ]


admin.site.register(User, UserAdmin)

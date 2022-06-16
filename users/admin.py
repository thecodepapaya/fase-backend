from django.contrib import admin
from django.http import HttpRequest

from users.actions.promote_user_to_faculty import promote_user_to_faculty

from .models import User


@admin.action(permissions=['change'])
def promote_to_faculty_role(modeladmin, request, queryset):

    for user in queryset:
        promote_user_to_faculty(user, request)
        # TODO send email with password


class UserAdmin(admin.ModelAdmin):
    list_display = ('institute_email', 'name', 'is_faculty')
    search_fields = ['name', 'institute_email', ]
    actions = [promote_to_faculty_role]

    def get_queryset(self, request: HttpRequest):
        user = request.user
        query_set = super().get_queryset(request)

        is_student = user.groups.filter(name="Student").exists()

        if is_student:
            filtered_query_set = query_set.filter(
                institute_email=user.institute_email)

        # Returning all users for faculty and SU
        else:
            filtered_query_set = query_set

        return filtered_query_set


admin.site.register(User, UserAdmin)

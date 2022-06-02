from django.contrib import admin

from .models import MetaData


class MetaAdmin(admin.ModelAdmin):
    list_display = ('min_app_version', 'min_app_build', )


admin.site.register(MetaData, MetaAdmin)

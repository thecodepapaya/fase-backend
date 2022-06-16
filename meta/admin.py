from django.contrib import admin

from .models import MetaData, DownloadLink


class MetaAdmin(admin.ModelAdmin):
    list_display = ('min_app_version', 'min_app_build', )


class DownloadAdmin(admin.ModelAdmin):
    list_display = ('id', 'apk_download', 'ios_download', 'created_at')


admin.site.register(MetaData, MetaAdmin)
admin.site.register(DownloadLink, DownloadAdmin)

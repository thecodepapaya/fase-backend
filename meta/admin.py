from django.contrib import admin

from .models import MetaData, MetaAdmin

admin.site.register(MetaData, MetaAdmin)

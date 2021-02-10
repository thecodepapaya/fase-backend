from django.db import models


class MetaData(models.Model):
    min_app_build = models.IntegerField(primary_key=True)
    min_app_version = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.min_app_version}({self.min_app_build})"

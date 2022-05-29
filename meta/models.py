from django.db import models


class MetaData(models.Model):
    min_app_build = models.IntegerField(primary_key=True)
    min_app_version = models.CharField(max_length=10)

    class Meta:
        ordering = ['-min_app_build']
        verbose_name_plural = "Meta Data"


    def __str__(self):
        return f"{self.min_app_version}({self.min_app_build})"

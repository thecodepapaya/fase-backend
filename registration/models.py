from django.contrib import admin
from django.db import models
from users.models import User


class Registration(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    """
        Fields related to device info
    """
    model = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    device_id = models.CharField(max_length=150)
    device_name = models.CharField(max_length=150)
    is_physical = models.BooleanField(default=True)
    is_rooted = models.BooleanField(default=False)

    """
        Fields related to application version data
    """
    app_version_string = models.CharField(max_length=10)
    app_build_number = models.IntegerField()

    """
        Fields related to Wifi info and local IP
    """
    ssid = models.CharField(max_length=100)
    bssid = models.CharField(max_length=100)
    local_ip = models.GenericIPAddressField()

    os = models.CharField(max_length=100)
    os_version = models.CharField(max_length=100)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.id)

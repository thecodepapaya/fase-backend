from django.contrib import admin
from django.db import models
from users.models import User


class Registration(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    """
        Fields related to device info
    """
    model = models.CharField(max_length=50)
    brand = models.CharField(max_length=20)
    device_id = models.CharField(max_length=50)
    device_name = models.CharField(max_length=100)
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
    ssid = models.CharField(max_length=32)
    bssid = models.CharField(max_length=23)
    local_ip = models.GenericIPAddressField()

    os = models.CharField(max_length=50)
    os_version = models.CharField(max_length=20)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.id)


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'student', 'timestamp')

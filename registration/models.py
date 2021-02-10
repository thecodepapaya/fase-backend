from django.db import models
from students.models import StudentData


class BasicData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    student_data = models.ForeignKey(StudentData, on_delete=models.CASCADE)

    """
        Fields related to device info
    """
    device_id = models.CharField(max_length=16)
    is_physical = models.BooleanField(default=True)
    is_rooted = models.BooleanField(default=False)
    # Long concat of brand/model/device/id/<something_i_don't_know>/type/tags
    # eg. google/sdk_gphone_x86_64/generic_x86_64_arm64:11/RSR1.201211.001/7027799:user/release-keys
    fingerprint = models.CharField(max_length=150)
    sdk_int = models.IntegerField()

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

    class Meta:
        abstract = True


class Registration(BasicData):
    registration_id = models.AutoField(primary_key=True, unique=True)
    server_key = models.CharField(max_length=40)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return "Registration ID: "+str(self.registration_id)+"\nStudent: "+str(self.student_data)+'\nDevice: '+str(self.device_id)

from django.db import models


class Faculty(models.Model):
    google_uid = models.CharField(max_length=15)
    institute_email = models.EmailField(max_length=40, primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"Name: {self.name} Email: {self.institute_email}"

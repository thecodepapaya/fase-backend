from django.db import models


class StudentData(models.Model):
    google_uid = models.CharField(max_length=15)
    institute_email = models.EmailField(max_length=28, primary_key=True)
    name = models.CharField(max_length=35)

    def __str__(self):
        return 'Name: '+self.name+'\nEmail: '+self.institute_email+'\nGoogle login ID'+self.google_uid

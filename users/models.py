from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class User(AbstractUser):
    institute_email = models.EmailField(max_length=80, primary_key=True)
    name = models.CharField(max_length=50)

    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'institute_email'

    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        # "Is the user a admin member?"
        return self.admin

    def __str__(self):
        return self.institute_email

import logging

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib import admin

from .managers import UserManager

logger = logging.getLogger(__file__)


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = None

    institute_email = models.EmailField(max_length=40, primary_key=True)
    name = models.CharField(max_length=50)
    display_picture = models.URLField(blank=True, null=True)

    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'institute_email'

    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    # def has_perm(self, perm, obj=None):
    #     # "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # @property
    # def is_admin(self):
    #     # "Is the user a admin member?"
    #     return self.admin

    @property
    def is_faculty(self):
        # Is the user a faculty
        has_faculty_group = self.groups.filter(name='Faculty').exists()
        logger.info(f'User has groups {self.groups}')

        return has_faculty_group

    def __str__(self):
        return f'{self.institute_email} - {self.name}'



class UserAdmin(admin.ModelAdmin):
    list_display = ('institute_email', 'name', 'is_faculty')

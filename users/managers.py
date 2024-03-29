from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import logging
logger = logging.getLogger(__file__)

"""  
    Custom user model manager where email is the unique identifiers  
    for authentication instead of usernames.  
    """


class UserManager(BaseUserManager):
    """  
    Custom user model manager where email is the unique identifiers  
    for authentication instead of usernames.  
    """

    def create_user(self, institute_email, password, **extra_fields):
        """  
        Create and save a User with the given email and password.  
        """
        if not institute_email:
            raise ValueError(_('The Email must be set'))
        institute_email = self.normalize_email(institute_email)
        logger.info('Creating user ======')
        logger.info(f'Password: {{password}}')
        user = self.model(institute_email=institute_email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, institute_email, password, **extra_fields):
        """  
        Create and save a SuperUser with the given email and password.  
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(institute_email, password, **extra_fields)

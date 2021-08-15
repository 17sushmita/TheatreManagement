from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    """
    class UserManager(BaseUserManager):
        def create_user(self,email, password=None):
            """
            Creates and saves a User with the given email, date of
            birth and password.
            """
            if not email:
                raise ValueError('Users must have an email address')

            user = self.model(
                email=self.normalize_email(email),
            )

            user.set_password(password)
            user.save(using=self._db)
            return user
        def create_superuser(self, email, password):
            """
            Creates and saves a superuser with the given email, date of
            birth and password.
            """
            user = self.create_user(
                email, password=password,
            )

            user.is_staff = True
            user.is_superuser = True

            user.save(using=self._db)
            return user

            
    email = models.EmailField(max_length=255, unique=True)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
from turtle import update
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid

# Create your CustomUserManager here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, password, first_name, last_name, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError("Phone Number must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password, first_name, last_name, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(password, first_name, last_name, phone_number, password, **extra_fields)

    def create_superuser(self, password, first_name, last_name, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(password, first_name, last_name, phone_number, **extra_fields)

# Create your User Model here.
class User(AbstractBaseUser,PermissionsMixin):
    # Abstractbaseuser has password, last_login, is_active by default

    user_id = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(db_index=True, max_length=50, unique=True)
    address = models.CharField(max_length=250)

    is_staff = models.BooleanField(default=True) # must needed, otherwise you won't be able to loginto django-admin.
    is_active = models.BooleanField(default=True) # must needed, otherwise you won't be able to loginto django-admin.
    is_superuser = models.BooleanField(default=False) # this field we inherit from PermissionsMixin.

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name','last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
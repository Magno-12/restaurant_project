from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

from apps.users.utils import ROLE
from apps.default.models.base_model import BaseModel
from apps.management.models.restaurant import Restaurant


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    # Basic user information
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        help_text='Este campo será usado para el login'
    )
    username = None  # Removemos el campo username
    
    # Contact information
    phone_number = PhoneNumberField(default='+1', blank=False, null=False)
    
    # Restaurant specific fields
    restaurant_code = models.CharField(
        max_length=6,
        help_text='6-digit code to identify the restaurant',
        null=True,
        blank=True
    )
    restaurant = models.ForeignKey(
        'management.Restaurant',
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )
    
    # Role and permissions
    role = models.CharField(
        choices=ROLE,
        blank=True,
        null=True,
        max_length=50,
        help_text='User role in the system'
    )
    is_restaurant_admin = models.BooleanField(
        default=False,
        help_text='Designates whether this user is an admin for their restaurant'
    )
    is_superadmin = models.BooleanField(
        default=False,
        help_text='Designates whether this user can manage all restaurants'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.email} ({self.get_full_name()})'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if self.is_superadmin:
            self.restaurant_code = None
            self.restaurant = None
        super().save(*args, **kwargs)

# Update related_name to avoid clashes
User._meta.get_field('groups').remote_field.related_name = 'user_set_custom'
User._meta.get_field('user_permissions').remote_field.related_name = 'user_set_custom_permissions'

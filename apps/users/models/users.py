from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

from apps.users.utils import ROLE
from apps.default.models.base_model import BaseModel
from apps.management.models.restaurant import Restaurant


class User(AbstractUser, BaseModel):
    # Basic user information
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        help_text='This field will be used for login'
    )
    # Remove username as primary login field
    username = None

    # Contact information
    phone_number = PhoneNumberField(default='+57', blank=False, null=False)

    # Restaurant specific fields
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True,
        help_text='Restaurant this user belongs to'
    )
    restaurant_code = models.CharField(
        max_length=6,
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(6)
        ],
        help_text='6-digit code to identify the restaurant',
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

    # Django auth settings
    EMAIL_FIELD = 'email'
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
        # Ensure superadmin doesn't have restaurant code or restaurant
        if self.is_superadmin:
            self.restaurant_code = None
            self.restaurant = None

        # Ensure restaurant_code matches restaurant's code if restaurant is set
        if self.restaurant and not self.restaurant_code:
            self.restaurant_code = self.restaurant.restaurant_code

        # Validate restaurant code matches restaurant if both are set
        if self.restaurant and self.restaurant_code:
            if self.restaurant.restaurant_code != self.restaurant_code:
                raise ValidationError("Restaurant code must match the assigned restaurant's code")

        super().save(*args, **kwargs)

# Update related_name to avoid clashes
User._meta.get_field('groups').remote_field.related_name = 'user_set_custom'
User._meta.get_field('user_permissions').remote_field.related_name = 'user_set_custom_permissions'

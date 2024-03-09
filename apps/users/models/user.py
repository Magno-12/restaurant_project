from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from apps.users.utils import ROLE
from apps.default.models.base_model import BaseModel


class User(AbstractUser, BaseModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone_number = PhoneNumberField(default='+1', blank=False, null=False)
    role = models.CharField(choices=ROLE, blank=True, null=True, max_length=50)

    def __str__(self):
        return f'{self.username}'

User._meta.get_field('groups').remote_field.related_name = 'user_set_custom'
User._meta.get_field('user_permissions').remote_field.related_name = 'user_set_custom_permissions'

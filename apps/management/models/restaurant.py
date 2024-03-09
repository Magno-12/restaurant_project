from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.default.models.base_model import BaseModel


class Restaurant(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = PhoneNumberField()
    email = models.EmailField()
    manager = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_restaurants'
    )
    opening_hours = models.CharField(max_length=255)
    website = models.URLField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

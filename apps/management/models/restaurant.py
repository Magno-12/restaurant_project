from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator, MaxLengthValidator

from apps.default.models.base_model import BaseModel


class Restaurant(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(  # Cambiado de restaurant_code a code
        max_length=6,
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(6)
        ],
        unique=True,
        help_text='Código único para identificar el restaurante'
    )
    address = models.TextField()
    phone = PhoneNumberField()
    email = models.EmailField()
    opening_hours = models.CharField(max_length=255)
    website = models.URLField()
    capacity = models.IntegerField()

    class Meta:
        app_label = 'management'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return f"{self.name} ({self.code})"

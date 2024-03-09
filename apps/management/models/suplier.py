from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from apps.default.models.base_model import BaseModel


class Supplier(BaseModel):
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    identification = models.CharField(max_length=255)
    cod = models.CharField(max_length=20, unique=True)
    phone = PhoneNumberField(default='+1', blank=False, null=False)
    email = models.EmailField()
    address = models.TextField()
    preferred_payment_method = models.CharField(max_length=100)

    def __str__(self):
        return self.name

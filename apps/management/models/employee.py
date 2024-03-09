from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.default.models.base_model import BaseModel
from apps.management.models.restaurant import Restaurant


class Employee(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = PhoneNumberField()
    hire_date = models.DateTimeField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    shift = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

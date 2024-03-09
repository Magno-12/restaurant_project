from django.db import models

from apps.default.models.base_model import BaseModel


class Customer(BaseModel):
    name = models.CharField(max_length=255)
    loyalty_points = models.IntegerField(default=0)
    preferred_dishes = models.TextField(blank=True)
    allergies = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'

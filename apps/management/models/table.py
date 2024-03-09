from django.db import models

from apps.default.models.base_model import BaseModel
from apps.management.models.restaurant import Restaurant


class Table(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    location = models.CharField(max_length=255)
    is_available = models.BooleanField()
    reservation_required = models.BooleanField()

    def __str__(self):
        return f'Table {self.id} in {self.restaurant.name}'

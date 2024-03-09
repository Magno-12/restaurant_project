# myapp/models/event.py
from django.db import models

from apps.default.models.base_model import BaseModel
from apps.management.models.restaurant import Restaurant
from apps.management.models.dish import Dish


class Event(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    special_menu = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True)
    expected_attendance = models.IntegerField()
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

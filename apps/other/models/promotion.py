from django.db import models

from apps.default.models.base_model import BaseModel
from apps.management.models.dish import Dish
from apps.management.models.restaurant import Restaurant


class Promotion(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    discount_percentage = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f'Promotion for {self.dish.name}'

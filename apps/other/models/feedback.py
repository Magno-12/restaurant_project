from django.db import models

from apps.default.models.base_model import BaseModel
from apps.users.models.customer import Customer
from apps.management.models.restaurant import Restaurant


class Feedback(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateTimeField()
    rating = models.IntegerField()
    comments = models.TextField(blank=True)

    def __str__(self):
        return f'Feedback by {self.customer}'

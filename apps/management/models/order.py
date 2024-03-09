from django.db import models

from apps.default.models.base_model import BaseModel
from apps.management.models.table import Table


class Order(BaseModel):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    order_date_time = models.DateTimeField()
    order_status = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)

    def __str__(self):
        return f'Order {self.id} at {self.table}'

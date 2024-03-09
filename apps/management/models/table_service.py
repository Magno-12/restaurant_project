from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.default.models.base_model import BaseModel
from apps.management.models.employee import Employee
from apps.management.models.table import Table


class TableService(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notes = models.TextField()

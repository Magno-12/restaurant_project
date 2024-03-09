from django.db import models

from apps.default.models.base_model import BaseModel


class Ingredient(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    unit_of_measure = models.CharField(max_length=100)
    allergen_info = models.TextField(blank=True)

    def __str__(self):
        return self.name

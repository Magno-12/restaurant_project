from django.db import models

from apps.default.models.base_model import BaseModel


class Ingredient(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    unit_of_measure = models.CharField(max_length=100)
    allergen_info = models.TextField(blank=True)
    minimum_required_quantity = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def is_below_minimum(self):
        inventory = self.inventory_set.first()
        if inventory:
            return inventory.available_quantity <= self.minimum_required_quantity
        return False

    def average_inventory(self):
        inventories = self.inventory_set.all()
        total_quantity = sum(inventory.available_quantity for inventory in inventories)
        count = inventories.count()
        if count > 0:
            return total_quantity / count
        return 0

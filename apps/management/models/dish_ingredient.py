from django.db import models
from decimal import Decimal

from apps.default.models.base_model import BaseModel
from apps.food.models.inventory import Inventory
from apps.management.models.dish import Dish


class DishIngredient(BaseModel):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='dish_ingredients')
    ingredient = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.dish.name} - {self.ingredient.name}"

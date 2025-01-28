from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.default.models.base_model import BaseModel
from apps.food.models.inventory import Inventory
from apps.management.models.dish import Dish


class DishIngredient(BaseModel):
    dish = models.ForeignKey(
        'management.Dish',  # Referencia lazy
        on_delete=models.CASCADE,
        related_name='dish_ingredients'
    )
    ingredient = models.ForeignKey(
        'food.Inventory',  # Referencia lazy
        on_delete=models.CASCADE,
        related_name='dish_ingredients'
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(
        'management.Restaurant',  # Referencia lazy
        on_delete=models.CASCADE,
        related_name='dish_ingredients'
    )

    class Meta:
        app_label = 'management'
        unique_together = ['dish', 'ingredient', 'restaurant']

    def clean(self):
        if self.dish.restaurant != self.ingredient.restaurant or self.dish.restaurant != self.restaurant:
            raise ValidationError('El plato, ingrediente y la relación deben pertenecer al mismo restaurante')

    def __str__(self):
        return f"{self.ingredient.product_name} para {self.dish.name} - {self.restaurant.name}"

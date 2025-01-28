# apps/food/models/inventory_ingredient.py
from django.db import models
from django.core.exceptions import ValidationError

from apps.default.models.base_model import BaseModel


class InventoryIngredient(BaseModel):
    inventory = models.ForeignKey(
        'food.Inventory',  # Referencia lazy
        on_delete=models.CASCADE,
        related_name='ingredient_entries'
    )
    ingredient = models.ForeignKey(
        'food.Ingredient',  # Referencia lazy
        on_delete=models.CASCADE,
        related_name='inventory_ingredients'
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(
        'management.Restaurant',  # Referencia lazy
        on_delete=models.CASCADE,
        related_name='inventory_ingredients'
    )

    class Meta:
        app_label = 'food'
        unique_together = ['inventory', 'ingredient', 'restaurant']

    def clean(self):
        if self.inventory.restaurant != self.ingredient.restaurant or self.inventory.restaurant != self.restaurant:
            raise ValidationError('El inventario, ingrediente y la entrada deben pertenecer al mismo restaurante')

    def __str__(self):
        return f"{self.ingredient.name} en {self.inventory.product_name} - {self.restaurant.name}"

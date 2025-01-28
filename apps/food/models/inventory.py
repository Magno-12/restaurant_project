from django.db import models
from decimal import Decimal

from apps.default.models.base_model import BaseModel

from apps.management.models.restaurant import Restaurant
from apps.food.models.ingredient import Ingredient
from apps.food.utils import CATEGORY_CHOICES


class InventoryIngredient(BaseModel):
    inventory = models.ForeignKey(
        'Inventory',
        on_delete=models.CASCADE,
        related_name='ingredient_entries'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='inventories'
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'food'

    def __str__(self):
        return f"{self.ingredient.name} in {self.inventory.product_name}"

class Inventory(BaseModel):
    product_name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=8, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    restaurant = models.ForeignKey(
        'management.Restaurant',
        on_delete=models.CASCADE,
        related_name='inventories'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through=InventoryIngredient,
        related_name='inventory_entries'
    )
    unit = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.FloatField()
    total_value = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    available_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_required_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'food'
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return f'{self.product_name}'

    def save(self, *args, **kwargs):
        if self.quantity is not None and self.unit_cost is not None:
            unit_cost_decimal = Decimal(str(self.unit_cost))
            self.total_value = self.quantity * unit_cost_decimal
        else:
            self.total_value = Decimal('0.00')
        super().save(*args, **kwargs)

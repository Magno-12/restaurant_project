from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

from apps.default.models.base_model import BaseModel
from apps.food.models.inventory import Inventory


class Dish(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(
        'management.Restaurant',  # Referencia lazy
        on_delete=models.CASCADE,
        related_name='dishes'
    )
    tax_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=Decimal('0.00'),
        help_text="Enter tax percentage (e.g., 10 for 10%)"
    )
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    net_sale_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    recipe_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    profit_margin = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        editable=False
    )
    available = models.BooleanField(default=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        app_label = 'management'
        unique_together = ['name', 'restaurant']

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

    def calculate_estimated_recipe_cost(self):
        total_cost = Decimal('0.00')
        for dish_ingredient in self.dish_ingredients.all():
            total_cost += dish_ingredient.quantity * Decimal(str(dish_ingredient.ingredient.unit_cost))
        return total_cost

    def save(self, *args, **kwargs):
        self.recipe_cost = self.calculate_estimated_recipe_cost()
        self.estimated_cost = self.recipe_cost
        tax_multiplier = self.tax_percentage / Decimal('100')
        self.sale_price = self.price + (self.price * tax_multiplier)
        if self.profit_margin is None:
            self.profit_margin = Decimal('0.00')
        profit_multiplier = self.profit_margin / Decimal('100')
        self.net_sale_price = self.price + (self.price * profit_multiplier)
        if self.recipe_cost and self.recipe_cost > 0:
            self.profit_margin = ((self.net_sale_price - self.recipe_cost) / self.recipe_cost) * Decimal('100')
        super().save(*args, **kwargs)

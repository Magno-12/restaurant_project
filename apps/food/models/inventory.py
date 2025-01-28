from django.db import models
from decimal import Decimal

from apps.default.models.base_model import BaseModel

from apps.management.models.restaurant import Restaurant
from apps.food.models.ingredient import Ingredient
from apps.food.utils import CATEGORY_CHOICES


# apps/food/models/inventory.py
from django.db import models
from decimal import Decimal
from apps.default.models.base_model import BaseModel
from apps.food.utils import CATEGORY_CHOICES

class Inventory(BaseModel):
    product_name = models.CharField(max_length=255)
    code = models.CharField(max_length=8)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    restaurant = models.ForeignKey(
        'management.Restaurant',
        on_delete=models.CASCADE,
        related_name='inventories'
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
        unique_together = ['product_name', 'restaurant', 'code']

    def __str__(self):
        return f'{self.product_name} - {self.restaurant.name}'

    def save(self, *args, **kwargs):
        if self.quantity is not None and self.unit_cost is not None:
            unit_cost_decimal = Decimal(str(self.unit_cost))
            self.total_value = self.quantity * unit_cost_decimal
        else:
            self.total_value = Decimal('0.00')
        super().save(*args, **kwargs)

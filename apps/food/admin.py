from django.contrib import admin

from apps.food.models.ingredient import Ingredient
from apps.food.models.inventory import Inventory


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    icon_name = 'free_breakfast'
    list_display = ('id', 'name', 'description', 'unit_of_measure', 'allergen_info', 'minimum_required_quantity', 'cost')
    # list_filter = ('unit_of_measure')
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at', 'is_below_minimum', 'average_inventory')

    def is_below_minimum(self, obj):
        return obj.is_below_minimum()
    is_below_minimum.boolean = True
    is_below_minimum.short_description = 'Below Minimum'

    def average_inventory(self, obj):
        return obj.average_inventory()
    average_inventory.short_description = 'Average Inventory'


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    icon_name = 'playlist_add'
    list_display = ('id', 'product_name', 'restaurant', 'available_quantity', 'minimum_required_quantity', 'last_updated')
    list_filter = ('restaurant',)
    search_fields = ('ingredient__name',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    fieldsets = (
        ('Dish Info', {
            'fields': (
                'code',
                'product_name',
                'category',
                'unit',
                'unit_cost',
                'quantity',
                'restaurant',
                'available_quantity',
                'minimum_required_quantity'
            )
        }),
        ('Status', {
            'fields': (
                'is_active',
            )
        }),
        ('Important Dates', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

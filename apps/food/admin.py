from django.contrib import admin

from apps.food.models.ingredient import Ingredient
from apps.food.models.inventory import Inventory


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    icon_name = 'free_breakfast'
    list_display = ('id', 'name', 'description', 'unit_of_measure', 'allergen_info')
    list_filter = ('unit_of_measure',)
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')


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

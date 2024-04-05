from django.contrib import admin

from apps.management.models.dish import Dish
from apps.management.models.employee import Employee
from apps.management.models.restaurant import Restaurant
from apps.management.models.order import Order
from apps.management.models.suplier import Supplier
from apps.management.models.table import Table
from apps.management.models.table_service import TableService
from apps.management.models.dish_ingredient import DishIngredient


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    icon_name = 'restaurant'
    list_display = ('id', 'name', 'address', 'phone', 'email', 'opening_hours', 'website', 'capacity')
    list_filter = ('is_active',)
    search_fields = ('name', 'address', 'phone', 'email')
    ordering = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    fieldsets = (
        ('Restaurant Info', {
            'fields': (
                'id',
                'name',
                'address',
                'phone',
                'email',
                'opening_hours',
                'website',
                'capacity'
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


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    icon_name = 'person_outline'
    list_display = ('id', 'first_name', 'last_name', 'role', 'restaurant', 'email', 'phone', 'hire_date', 'salary', 'shift')
    list_filter = ('role', 'restaurant', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    ordering = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    fieldsets = (
        ('Employee Info', {
            'fields': (
                'id',
                'first_name',
                'last_name',
                'role',
                'restaurant',
                'email',
                'phone',
                'hire_date',
                'salary',
                'shift'
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


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    icon_name = 'restaurant_menu'
    # Asegúrate de que 'list_display' incluye todos los campos relevantes
    list_display = (
        'id', 'name', 'description', 'price', 'tax_percentage',
        'sale_price', 'net_sale_price', 'recipe_cost', 'profit_margin', 'available'
    )
    list_filter = ('available',)  # 'list_filter' acepta una tupla o lista
    search_fields = ('name', 'description')
    ordering = ('id',)
    # Los campos calculados y el ID deben ser de solo lectura
    readonly_fields = (
        'id', 'created_at', 'updated_at', 'sale_price',
        'net_sale_price', 'recipe_cost', 'profit_margin'
    )

    # Asegúrate de que 'fieldsets' contiene todos los campos necesarios, tanto editables como de solo lectura
    fieldsets = (
        ('Dish Info', {
            'fields': (
                'name',
                'description',
                'price',
                'tax_percentage',
                'ingredients',
                'available'
            )
        }),
        ('Financial', {
            'fields': (
                'sale_price',
                'net_sale_price',
                'recipe_cost',
                'profit_margin',
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


@admin.register(DishIngredient)
class DishIngredientAdmin(admin.ModelAdmin):
    icon_name = 'restaurant'
    list_display = ('id', 'dish', 'ingredient', 'quantity')
    list_filter = ('dish', 'ingredient')
    search_fields = ('dish__name', 'ingredient__name')
    ordering = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    fieldsets = (
        ('Dish Ingredient Info', {
            'fields': (
                'dish',
                'ingredient',
                'quantity',
            )
        }),
        ('Important Dates', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    icon_name = 'reorder'
    list_display = ('id', 'table', 'order_date_time', 'order_status', 'total_amount', 'payment_method')
    list_filter = ('order_status', 'payment_method')
    search_fields = ('table__id',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    icon_name = 'supervisor_account'
    list_display = ('id', 'name', 'contact_name', 'phone', 'email', 'address', 'preferred_payment_method')
    list_filter = ('preferred_payment_method',)
    search_fields = ('name', 'contact_name', 'email', 'phone')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    icon_name = 'tab'
    list_display = ('id', 'restaurant', 'capacity', 'location', 'is_available', 'reservation_required')
    list_filter = ('restaurant', 'is_available', 'reservation_required')
    search_fields = ('location',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    fieldsets = (
        ('Table Information', {
            'fields': (
                'restaurant',
                'capacity',
                'location',
                'is_available',
                'reservation_required'
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


@admin.register(TableService)
class TableServiceAdmin(admin.ModelAdmin):
    icon_name = 'room_service'
    list_display = ('id', 'employee', 'table', 'start_time', 'end_time', 'notes')
    list_filter = ('employee', 'table')
    search_fields = ('notes',)
    readonly_fields = ('id', 'created_at', 'updated_at')

    fieldsets = (
        ('Table Service Information', {
            'fields': (
                'employee',
                'table',
                'start_time',
                'end_time',
                'notes'
            )
        }),
        ('Important Dates', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

from rest_framework import serializers

from apps.management.models import Table, Employee
from apps.management.models.dish import Dish
from apps.management.models.order import Order, OrderItem


class TableSerializer(serializers.ModelSerializer):
    current_server_name = serializers.CharField(source='current_server.get_full_name', read_only=True)
    
    class Meta:
        model = Table
        fields = ['id', 'table_number', 'status', 'capacity', 'current_server', 
                 'current_server_name', 'occupied_since', 'location']
        read_only_fields = ['restaurant']


# serializers/order_serializer.py
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'dish', 'quantity', 'unit_price', 'notes', 'status']
        read_only_fields = ['order']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    server_name = serializers.CharField(source='server.get_full_name', read_only=True)
    table_number = serializers.CharField(source='table.table_number', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'table', 'table_number', 'server', 'server_name', 
                 'status', 'items', 'subtotal', 'tax', 'total', 'payment_status']
        read_only_fields = ['server']


class OrderCreateSerializer(serializers.Serializer):
    table_id = serializers.IntegerField()
    number_of_guests = serializers.IntegerField(min_value=1)


# serializers/dish_serializer.py
class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = [
            'id', 
            'name', 
            'description', 
            'price', 
            'available', 
            'sale_price',
            'tax_percentage',
            'recipe_cost',
            'profit_margin'
        ]
        read_only_fields = [
            'restaurant',
            'sale_price',
            'recipe_cost',
            'profit_margin'
        ]


class CategorySerializer(serializers.Serializer):
    id = serializers.CharField()  # Este será el valor de la categoría
    name = serializers.CharField()  # Este será el display name de la categoría
    dish_count = serializers.IntegerField(read_only=True)

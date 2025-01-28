# views/table_view.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.management.models import Table
from apps.management.serializers.management_serializer import *
from apps.management.permissions import BelongsToRestaurantPermission

class TableViewSet(GenericViewSet):
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated, BelongsToRestaurantPermission]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # Detectar generación de esquema
            return Table.objects.none()
        return Table.objects.filter(restaurant=self.request.user.restaurant)

    @swagger_auto_schema(
        operation_description="Lista todas las mesas del restaurante"
    )
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Obtiene una mesa específica"
    )
    def retrieve(self, request, pk=None):
        table = self.get_object()
        serializer = self.get_serializer(table)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Actualiza el estado de una mesa",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        table = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Table.TABLE_STATUS):
            return Response(
                {'error': 'Estado inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        table.status = new_status
        table.save()
        return Response(self.get_serializer(table).data)

# views/order_view.py
class OrderViewSet(GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, BelongsToRestaurantPermission]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # Detectar generación de esquema
            return Order.objects.none()
        return Order.objects.filter(table__restaurant=self.request.user.restaurant)

    def get_serializer_class(self):
        if self.action == 'create_order':
            return OrderCreateSerializer
        return self.serializer_class

    @swagger_auto_schema(
        operation_description="Crea una nueva orden",
        request_body=OrderCreateSerializer
    )
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        table = Table.objects.get(
            id=serializer.validated_data['table_id'],
            restaurant=request.user.restaurant
        )
        
        order = Order.objects.create(
            table=table,
            server=request.user,
            status='open',
            number_of_guests=serializer.validated_data['number_of_guests']
        )
        
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        operation_description="Añade items a una orden",
        request_body=OrderItemSerializer
    )
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['open', 'in_progress']:
            return Response(
                {'error': 'No se pueden añadir items a esta orden'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verificar que el plato pertenece al mismo restaurante
        dish = serializer.validated_data['dish']
        if dish.restaurant != request.user.restaurant:
            return Response(
                {'error': 'Plato no pertenece a este restaurante'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        item = OrderItem.objects.create(
            order=order,
            **serializer.validated_data
        )
        
        return Response(
            OrderItemSerializer(item).data,
            status=status.HTTP_201_CREATED
        )

# views/dish_view.py
class DishViewSet(GenericViewSet):
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated, BelongsToRestaurantPermission]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # Detectar generación de esquema
            return Dish.objects.none()
        return Dish.objects.filter(
            restaurant=self.request.user.restaurant,
            available=True
        )

    @swagger_auto_schema(
        operation_description="Lista todos los platos disponibles"
    )
    def list(self, request):
        category = request.query_params.get('category')
        search = request.query_params.get('search')
        
        queryset = self.get_queryset()
        
        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(name__icontains=search)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

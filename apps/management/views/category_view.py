from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from apps.management.permissions import *
from apps.food.utils import CATEGORY_CHOICES
from apps.management.models import Dish
from apps.management.serializers.management_serializer import CategorySerializer


class CategoryViewSet(GenericViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, BelongsToRestaurantPermission]

    def list(self, request):
        """Lista todas las categorías disponibles con el conteo de platos."""
        restaurant = request.user.restaurant

        # Obtener el conteo de platos por categoría
        dish_counts = Dish.objects.filter(
            restaurant=restaurant,
            available=True
        ).values('category').annotate(
            count=Count('id')
        ).order_by('category')

        # Crear un diccionario con los conteos
        count_dict = {
            item['category']: item['count']
            for item in dish_counts
        }

        # Preparar los datos de las categorías
        categories_data = [
            {
                'id': category_id,
                'name': category_name,
                'dish_count': count_dict.get(category_id, 0)
            }
            for category_id, category_name in CATEGORY_CHOICES
        ]

        serializer = self.get_serializer(categories_data, many=True)
        return Response(serializer.data)

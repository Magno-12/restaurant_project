# apps/management/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.management.views.management_view import *
from apps.management.views.category_view import CategoryViewSet

# Crear router
router = DefaultRouter()

# Registrar viewsets
router.register(r'tables', TableViewSet, basename='table')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'dishes', DishViewSet, basename='dish')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]

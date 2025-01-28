# apps/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication.views.authentication_view import AuthenticationViewSet

# Crear router
router = DefaultRouter()

# Registrar viewset de autenticación
router.register(r'auth', AuthenticationViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    # Ruta para refrescar token JWT
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

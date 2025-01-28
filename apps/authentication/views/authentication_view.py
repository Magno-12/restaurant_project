from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from apps.users.models import User
from apps.management.models import Restaurant
from apps.authentication.serializers.authentication_serializer import *


class AuthenticationViewSet(GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'login':
            return AuthenticationSerializer
        elif self.action == 'verify_restaurant_code':
            return RestaurantCodeSerializer
        return LogoutSerializer

    @swagger_auto_schema(
        operation_description="Inicia sesión de usuario",
        request_body=AuthenticationSerializer,
        responses={
            200: openapi.Response(
                description="Login exitoso",
                schema=UserAuthResponseSerializer
            ),
            401: "Credenciales inválidas"
        }
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data

        try:
            user = User.objects.get(email=user_data['email'])
        except User.DoesNotExist:
            raise AuthenticationFailed("Credenciales inválidas")

        if not check_password(user_data['password'], user.password):
            raise AuthenticationFailed("Credenciales inválidas")

        if not user.is_active:
            raise AuthenticationFailed("Esta cuenta ha sido desactivada")

        # Si se proporciona código de restaurante, verificar
        restaurant_code = user_data.get('restaurant_code')
        if restaurant_code:
            try:
                restaurant = Restaurant.objects.get(code=restaurant_code)
                if user.restaurant and user.restaurant != restaurant:
                    raise AuthenticationFailed("Código de restaurante inválido")
                user.restaurant = restaurant
                user.save()
            except Restaurant.DoesNotExist:
                raise AuthenticationFailed("Código de restaurante inválido")

        # Generar token que expire en 24 horas
        refresh = RefreshToken.for_user(user)
        refresh.access_token.set_exp(lifetime=timezone.timedelta(hours=24))

        response_data = {
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "user": UserAuthResponseSerializer(user).data
        }

        # Si el usuario necesita verificar código de restaurante
        if not user.restaurant and not user.is_superadmin:
            response_data["requires_restaurant_code"] = True

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Verifica el código del restaurante",
        request_body=RestaurantCodeSerializer,
        responses={
            200: "Código verificado exitosamente",
            400: "Código inválido"
        }
    )
    @action(detail=False, methods=['post'])
    def verify_restaurant_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            restaurant = Restaurant.objects.get(code=serializer.validated_data['code'])
            user = request.user
            user.restaurant = restaurant
            user.save()
            
            return Response({
                "message": "Código verificado exitosamente",
                "restaurant": {
                    "id": restaurant.id,
                    "name": restaurant.name,
                    "code": restaurant.code
                }
            }, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response(
                {"error": "Código de restaurante inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_description="Cierra la sesión del usuario",
        request_body=LogoutSerializer,
        responses={
            200: "Sesión cerrada exitosamente",
            400: "Token inválido"
        }
    )
    @action(detail=False, methods=['post'])
    def logout(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            token = RefreshToken(serializer.validated_data['refresh_token'])
            token.blacklist()
            return Response(
                {"message": "Sesión cerrada exitosamente"},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error": "Token inválido o expirado"},
                status=status.HTTP_400_BAD_REQUEST
            )

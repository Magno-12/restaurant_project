from rest_framework import serializers

from apps.users.models import User


class AuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    restaurant_code = serializers.CharField(required=False)

class RestaurantCodeSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserAuthResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 
                 'restaurant_code', 'is_restaurant_admin', 'is_superadmin']

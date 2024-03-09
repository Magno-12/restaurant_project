from django.contrib import admin

from apps.users.models.user import User
from apps.users.models.customer import Customer


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'role')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    ordering = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets =(
        ('User', {
            'fields': (
                 'id',
                 'username',
                 'first_name',
                 'last_name',
                 'email',
                 'phone_number',
                 'role',
                )
            }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                )
            }),
        ('Important dates', {
            'fields': (
                'created_at',
                'updated_at',
                )
            }),
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'loyalty_points')
    readonly_fields = ('id', 'created_at', 'updated_at')

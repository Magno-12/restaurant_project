from django.contrib import admin

from apps.other.models.event import Event
from apps.other.models.feedback import Feedback
from apps.other.models.promotion import Promotion


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    icon_name = 'event'
    list_display = ('id', 'restaurant', 'name', 'description', 'start_date_time', 'end_date_time', 'special_menu', 'expected_attendance', 'entry_fee')
    list_filter = ('restaurant',)
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    icon_name = 'redeem'
    list_display = ('id', 'restaurant', 'dish', 'start_date', 'end_date', 'discount_percentage', 'description')
    list_filter = ('restaurant', 'start_date', 'end_date')
    search_fields = ('dish__name',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    icon_name = 'feedback'
    list_display = ('id', 'customer', 'restaurant', 'date', 'rating', 'comments')
    list_filter = ('restaurant', 'rating')
    search_fields = ('customer__first_name', 'customer__last_name')
    readonly_fields = ('id', 'created_at', 'updated_at')

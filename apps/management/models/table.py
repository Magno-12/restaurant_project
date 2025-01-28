from django.db import models
from django.core.exceptions import ValidationError

from apps.default.models.base_model import BaseModel
from apps.management.models.restaurant import Restaurant
from apps.management.models.employee import Employee


class Table(BaseModel):
    # Table status choices
    TABLE_STATUS = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('cleaning', 'Being Cleaned'),
        ('maintenance', 'Under Maintenance'),
    ]

    # Basic table information
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='tables'
    )
    table_number = models.CharField(
        max_length=10,
        help_text='Unique identifier for the table within the restaurant'
    )
    capacity = models.IntegerField(
        help_text='Maximum number of guests that can be seated'
    )
    
    # Location and arrangement
    location = models.CharField(
        max_length=255,
        help_text='Location description (e.g., "Outdoor", "Main Hall", "Second Floor")'
    )
    
    # Status and availability
    status = models.CharField(
        max_length=20,
        choices=TABLE_STATUS,
        default='available',
        help_text='Current status of the table'
    )
    current_server = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tables',
        help_text='Server currently assigned to this table'
    )
    
    # Reservation settings
    reservation_required = models.BooleanField(
        default=False,
        help_text='Whether this table requires reservation'
    )
    
    # Timestamps for status changes
    status_changed_at = models.DateTimeField(
        auto_now=True,
        help_text='Last time the status was changed'
    )
    occupied_since = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the table was last occupied'
    )

    class Meta:
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'
        unique_together = ['restaurant', 'table_number']
        ordering = ['table_number']

    def __str__(self):
        return f'Table {self.table_number} - {self.restaurant.name}'

    def clean(self):
        # Validate server belongs to the same restaurant
        if self.current_server and self.current_server.restaurant != self.restaurant:
            raise ValidationError({
                'current_server': 'Server must belong to the same restaurant as the table'
            })

    def save(self, *args, **kwargs):
        self.clean()
        # Update occupied_since when status changes to occupied
        if self.status == 'occupied' and (
            not self.occupied_since or 
            self._state.adding or 
            self._state.fields_cache.get('status', None) != 'occupied'
        ):
            from django.utils import timezone
            self.occupied_since = timezone.now()
        # Clear occupied_since when table becomes available
        elif self.status != 'occupied':
            self.occupied_since = None
        super().save(*args, **kwargs)

    def is_available(self):
        """Check if table can be seated"""
        return self.status == 'available'

    def get_current_order(self):
        """Get the current active order for this table"""
        return self.orders.filter(
            status__in=['open', 'in_progress']
        ).first()

    def change_status(self, new_status, server=None):
        """
        Change table status and optionally assign a server
        Returns True if status was changed successfully
        """
        if new_status not in dict(self.TABLE_STATUS):
            return False

        self.status = new_status
        if server:
            self.current_server = server
        self.save()
        return True

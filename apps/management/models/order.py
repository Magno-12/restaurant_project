from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.default.models.base_model import BaseModel
from apps.management.models.table import Table
from apps.management.models.employee import Employee
from apps.management.models.dish import Dish


class OrderItem(BaseModel):
    """Model for individual items in an order"""
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='items'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Price at the time of order'
    )
    notes = models.TextField(
        blank=True,
        help_text='Special instructions or modifications'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('preparing', 'Preparing'),
            ('ready', 'Ready to Serve'),
            ('served', 'Served'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f'{self.quantity}x {self.dish.name}'

    def save(self, *args, **kwargs):
        # Set initial price from dish if not set
        if not self.unit_price:
            self.unit_price = self.dish.price
        super().save(*args, **kwargs)

class Order(BaseModel):
    # Order status choices
    ORDER_STATUS = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('ready', 'Ready to Serve'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    # Payment status choices
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('refunded', 'Refunded')
    ]

    # Payment method choices
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('mobile_payment', 'Mobile Payment')
    ]

    # Basic order information
    table = models.ForeignKey(
        Table,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    server = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='orders_served'
    )

    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='open'
    )

    # Timestamps
    order_time = models.DateTimeField(
        auto_now_add=True,
        help_text='When the order was created'
    )
    completed_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the order was completed or cancelled'
    )

    # Guest information
    number_of_guests = models.PositiveIntegerField(
        default=1,
        help_text='Number of guests at the table'
    )

    # Payment information
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        null=True,
        blank=True
    )

    # Amounts
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Sum of all items before tax and tip'
    )
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    tip = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Final amount including tax and tip'
    )

    # Additional information
    notes = models.TextField(
        blank=True,
        help_text='General notes about the order'
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-order_time']

    def __str__(self):
        return f'Order #{self.id} - Table {self.table.table_number}'

    def clean(self):
        # Validate server belongs to same restaurant as table
        if self.server.restaurant != self.table.restaurant:
            raise ValidationError({
                'server': 'Server must belong to the same restaurant as the table'
            })

    def save(self, *args, **kwargs):
        self.clean()

        # Calculate totals
        self.subtotal = sum(
            item.quantity * item.unit_price 
            for item in self.items.all()
        )

        # Assuming tax rate is stored in restaurant settings
        tax_rate = self.table.restaurant.tax_rate if hasattr(self.table.restaurant, 'tax_rate') else Decimal('0.00')
        self.tax = self.subtotal * tax_rate

        # Calculate total
        self.total = self.subtotal + self.tax + self.tip

        # Set completed time if status is completed or cancelled
        if self.status in ['completed', 'cancelled'] and not self.completed_time:
            from django.utils import timezone
            self.completed_time = timezone.now()

        super().save(*args, **kwargs)

    def add_item(self, dish, quantity=1, notes=''):
        """Add a new item to the order"""
        if self.status not in ['open', 'in_progress']:
            raise ValidationError('Cannot add items to a completed or cancelled order')

        return OrderItem.objects.create(
            order=self,
            dish=dish,
            quantity=quantity,
            unit_price=dish.price,
            notes=notes
        )

    def remove_item(self, item_id):
        """Remove an item from the order"""
        if self.status not in ['open', 'in_progress']:
            raise ValidationError('Cannot remove items from a completed or cancelled order')

        try:
            item = self.items.get(id=item_id)
            item.delete()
            return True
        except OrderItem.DoesNotExist:
            return False

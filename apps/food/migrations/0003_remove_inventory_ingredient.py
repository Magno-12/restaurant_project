# Generated by Django 4.2.4 on 2023-12-07 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_inventory_category_inventory_code_inventory_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='ingredient',
        ),
    ]
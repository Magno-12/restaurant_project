# Generated by Django 4.2.4 on 2023-12-07 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_inventory_category_inventory_code_inventory_quantity_and_more'),
        ('management', '0002_supplier_cod_supplier_identification'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='ingredients',
            field=models.ManyToManyField(related_name='dishes', to='food.ingredient'),
        ),
    ]

# Generated by Django 4.2.4 on 2023-12-07 14:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('unit_of_measure', models.CharField(max_length=100)),
                ('allergen_info', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('available_quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('minimum_required_quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('last_updated', models.DateTimeField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.ingredient')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.restaurant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

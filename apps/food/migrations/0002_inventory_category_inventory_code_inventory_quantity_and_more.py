# Generated by Django 4.2.4 on 2023-12-07 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='category',
            field=models.CharField(choices=[('oils', 'Oils'), ('dairy', 'Dairy'), ('wines', 'Wines'), ('meats', 'Meats'), ('fish', 'Fish'), ('frozen', 'Frozen')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='code',
            field=models.CharField(default=1, max_length=8, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='total_value',
            field=models.DecimalField(decimal_places=2, default=1, editable=False, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='unit',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='unit_cost',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
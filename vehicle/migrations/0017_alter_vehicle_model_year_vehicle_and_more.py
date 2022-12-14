# Generated by Django 4.1.3 on 2023-01-06 10:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0016_vehicle_other_data_vehicle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='model_year_vehicle',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1890)], verbose_name='ano do modelo'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='year_manufacture_vehicle',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1890)], verbose_name='ano de fabricação'),
        ),
    ]

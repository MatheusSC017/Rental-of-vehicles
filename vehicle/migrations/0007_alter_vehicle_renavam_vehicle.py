# Generated by Django 4.1 on 2022-08-27 18:08

from django.db import migrations, models
from utils import validators


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0006_vehicle_renavam_vehicle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='renavam_vehicle',
            field=models.CharField(max_length=11, validators=[validators.docbr.RENAVAMValidator()], verbose_name='renavam'),
        ),
    ]

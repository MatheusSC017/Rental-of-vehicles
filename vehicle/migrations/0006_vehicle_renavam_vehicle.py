# Generated by Django 4.1 on 2022-08-27 18:02

from django.db import migrations, models
from utils import validators


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0005_rename_year_manufacure_vehicle_vehicle_year_manufacture_vehicle'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='renavam_vehicle',
            field=models.CharField(default='11212213132', max_length=11, validators=[
                validators.docbr.RENAVAMValidator], verbose_name='renavam'),
            preserve_default=False,
        ),
    ]

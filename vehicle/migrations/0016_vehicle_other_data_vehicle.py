# Generated by Django 4.1 on 2022-09-23 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0015_remove_vehicle_other_data_vehicle'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='other_data_vehicle',
            field=models.JSONField(blank=True, null=True, verbose_name='mais informações'),
        ),
    ]

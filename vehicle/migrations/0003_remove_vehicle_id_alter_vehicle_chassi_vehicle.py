# Generated by Django 4.1 on 2022-08-23 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0002_vehicle_available_vehicle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='id',
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='chassi_vehicle',
            field=models.CharField(max_length=17, primary_key=True, serialize=False, verbose_name='chassi'),
        ),
    ]
# Generated by Django 5.0.1 on 2024-02-04 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0006_address_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='is_active',
        ),
    ]

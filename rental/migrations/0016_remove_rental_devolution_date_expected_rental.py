# Generated by Django 4.1.3 on 2022-12-13 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0015_rename_devolution_date_expected_rental_devolution_date_expected_rental'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rental',
            name='devolution_date_expected_rental',
        ),
    ]

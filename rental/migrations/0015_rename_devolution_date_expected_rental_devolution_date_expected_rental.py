# Generated by Django 4.1.3 on 2022-12-03 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0014_rental_devolution_date_expected_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rental',
            old_name='devolution_date_expected',
            new_name='devolution_date_expected_rental',
        ),
    ]

# Generated by Django 4.1.3 on 2023-12-15 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_alter_address_cep_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='cep_address',
            new_name='cep',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='city_address',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='district_address',
            new_name='district',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='number_address',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='state_address',
            new_name='state',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='street_address',
            new_name='street',
        ),
    ]

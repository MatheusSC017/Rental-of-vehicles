# Generated by Django 4.1 on 2022-08-31 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_rename_address_client_client_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='address',
            new_name='address_person',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='age',
            new_name='age_person',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='cpf',
            new_name='cpf_person',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='gender',
            new_name='gender_person',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='phone',
            new_name='phone_person',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='rg',
            new_name='rg_person',
        ),
    ]
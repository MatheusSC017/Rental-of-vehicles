# Generated by Django 4.1 on 2022-08-25 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_alter_address_state_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='cep_address',
            field=models.CharField(max_length=9, verbose_name='CEP'),
        ),
    ]
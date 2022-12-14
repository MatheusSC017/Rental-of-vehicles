# Generated by Django 4.1 on 2022-08-20 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep_address', models.CharField(max_length=8, verbose_name='CEP')),
                ('state_address', models.CharField(max_length=2, verbose_name='estado (sigla)')),
                ('city_address', models.CharField(max_length=100, verbose_name='cidade')),
                ('district_address', models.CharField(max_length=100, verbose_name='bairro')),
                ('street_address', models.CharField(max_length=100, verbose_name='rua')),
                ('number_address', models.CharField(max_length=30, verbose_name='número')),
            ],
        ),
    ]

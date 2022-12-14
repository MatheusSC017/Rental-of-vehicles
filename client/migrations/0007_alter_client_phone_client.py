# Generated by Django 4.1 on 2022-08-28 14:01

from django.db import migrations, models
from utils import validators


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_alter_client_age_client_alter_client_phone_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_client',
            field=models.CharField(max_length=16, validators=[validators.basic_user.PhoneValidator()], verbose_name='telefone'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-04 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0004_alter_branch_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
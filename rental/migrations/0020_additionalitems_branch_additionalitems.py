# Generated by Django 4.1.3 on 2023-01-05 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0002_rename_opening_hours_end_branch_opening_hours_end_branch_and_more'),
        ('rental', '0019_remove_rental_additional_items_rental_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalitems',
            name='branch_additionalitems',
            field=models.ForeignKey(default=42, on_delete=django.db.models.deletion.DO_NOTHING, to='branch.branch', verbose_name='filial'),
            preserve_default=False,
        ),
    ]

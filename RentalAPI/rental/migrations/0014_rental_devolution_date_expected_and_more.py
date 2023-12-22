# Generated by Django 4.1.3 on 2022-12-03 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0016_vehicle_other_data_vehicle'),
        ('rental', '0013_alter_rental_additional_items_rental'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='devolution_date_expected',
            field=models.DateField(default='2022-12-12', verbose_name='data de devolução esperada'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rental',
            name='vehicle_rental',
            field=models.ForeignKey(limit_choices_to={'available_vehicle': True}, on_delete=django.db.models.deletion.DO_NOTHING, to='vehicle.vehicle', verbose_name='veículo'),
        ),
    ]
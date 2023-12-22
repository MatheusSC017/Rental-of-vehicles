# Generated by Django 4.1.3 on 2023-12-15 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0017_alter_vehicle_model_year_vehicle_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='available_vehicle',
            new_name='available',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='branch_vehicle',
            new_name='branch',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='brand_vehicle',
            new_name='brand',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='chassi_vehicle',
            new_name='chassi',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='classification_vehicle',
            new_name='classification',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='color_vehicle',
            new_name='color',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='engine_vehicle',
            new_name='engine',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='fuel_vehicle',
            new_name='fuel',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='fuel_tank_vehicle',
            new_name='fuel_tank',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='image_vehicle',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='license_plate_vehicle',
            new_name='license_plate',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='mileage_vehicle',
            new_name='mileage',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='model_vehicle',
            new_name='model',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='model_year_vehicle',
            new_name='model_year',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='other_data_vehicle',
            new_name='other_data',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='renavam_vehicle',
            new_name='renavam',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='type_vehicle',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='year_manufacture_vehicle',
            new_name='year_manufacture',
        ),
        migrations.RenameField(
            model_name='vehicleclassification',
            old_name='daily_cost_classification',
            new_name='daily_cost',
        ),
        migrations.RenameField(
            model_name='vehicleclassification',
            old_name='title_classification',
            new_name='title',
        ),
    ]
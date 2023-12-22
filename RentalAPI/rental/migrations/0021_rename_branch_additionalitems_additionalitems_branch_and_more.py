# Generated by Django 4.1.3 on 2023-12-15 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0003_rename_address_branch_branch_address_and_more'),
        ('client', '0011_rename_address_person_client_address_and_more'),
        ('vehicle', '0018_rename_available_vehicle_vehicle_available_and_more'),
        ('rental', '0020_additionalitems_branch_additionalitems'),
    ]

    operations = [
        migrations.RenameField(
            model_name='additionalitems',
            old_name='branch_additionalitems',
            new_name='branch',
        ),
        migrations.RenameField(
            model_name='additionalitems',
            old_name='daily_cost_additionalitems',
            new_name='daily_cost',
        ),
        migrations.RenameField(
            model_name='additionalitems',
            old_name='name_additionalitems',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='additionalitems',
            old_name='stock_additionalitems',
            new_name='stock',
        ),
        migrations.RenameField(
            model_name='insurance',
            old_name='coverage_insurance',
            new_name='coverage',
        ),
        migrations.RenameField(
            model_name='insurance',
            old_name='price_insurance',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='insurance',
            old_name='title_insurance',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='actual_days_rental',
            new_name='actual_days',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='additional_daily_cost_rental',
            new_name='additional_daily_cost',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='appointment_date_rental',
            new_name='appointment_date',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='daily_cost_rental',
            new_name='daily_cost',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='devolution_date_rental',
            new_name='devolution_date',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='distance_branch_rental',
            new_name='distance_branch',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='fines_rental',
            new_name='fines',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='insurance_rental',
            new_name='insurance',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='rent_date_rental',
            new_name='rent_date',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='rent_deposit_rental',
            new_name='rent_deposit',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='requested_days_rental',
            new_name='requested_days',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='return_rate_rental',
            new_name='return_rate',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='staff_rental',
            new_name='staff',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='status_rental',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='rental',
            old_name='total_cost_rental',
            new_name='total_cost',
        ),
        migrations.RenameField(
            model_name='rentaladditionalitem',
            old_name='additional_item_relationship',
            new_name='additional_item',
        ),
        migrations.RenameField(
            model_name='rentaladditionalitem',
            old_name='number_relationship',
            new_name='number',
        ),
        migrations.AlterUniqueTogether(
            name='rentaladditionalitem',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='rental',
            name='arrival_branch_rental',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='client_rental',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='driver_rental',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='outlet_branch_rental',
        ),
        migrations.RemoveField(
            model_name='rental',
            name='vehicle_rental',
        ),
        migrations.AddField(
            model_name='rental',
            name='arrival_branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='arrival_branch', to='branch.branch', verbose_name='filial de chegada'),
        ),
        migrations.AddField(
            model_name='rental',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='client', to='client.client', verbose_name='cliente'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rental',
            name='driver',
            field=models.ManyToManyField(related_name='driver', to='client.client', verbose_name='condutores'),
        ),
        migrations.AddField(
            model_name='rental',
            name='outlet_branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='outlet_branch', to='branch.branch', verbose_name='filial de saída'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rental',
            name='vehicle',
            field=models.ForeignKey(default=1, limit_choices_to={'available': True}, on_delete=django.db.models.deletion.DO_NOTHING, to='vehicle.vehicle', verbose_name='veículo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rentaladditionalitem',
            name='rental',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='additional_items', to='rental.rental', verbose_name='Aluguel'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='rentaladditionalitem',
            unique_together={('rental', 'additional_item')},
        ),
        migrations.RemoveField(
            model_name='rentaladditionalitem',
            name='rental_relationship',
        ),
    ]
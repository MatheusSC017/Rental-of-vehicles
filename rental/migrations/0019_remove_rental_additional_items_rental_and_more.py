# Generated by Django 4.1.3 on 2022-12-16 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0018_alter_additionalitems_stock_additionalitems'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rental',
            name='additional_items_rental',
        ),
        migrations.CreateModel(
            name='RentalAdditionalItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_relationship', models.PositiveSmallIntegerField(default=1, verbose_name='Número de itens')),
                ('additional_item_relationship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental.additionalitems', verbose_name='Item adicional')),
                ('rental_relationship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental.rental', verbose_name='Aluguel')),
            ],
            options={
                'unique_together': {('rental_relationship', 'additional_item_relationship')},
            },
        ),
    ]

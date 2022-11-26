from django.db import models
from django.core.validators import MinValueValidator
from branch.models import Branch
from validators.docbr import RENAVAMValidator


class VehicleClassification(models.Model):
    title_classification = models.CharField(max_length=50, verbose_name='classificação')
    daily_cost_classification = models.FloatField(validators=[MinValueValidator(0)], verbose_name='custo da diária')

    def __str__(self):
        return self.title_classification

    def __repr__(self):
        return self.id

    class Meta:
        verbose_name = 'classificação'
        verbose_name_plural = 'classificações'


class Vehicle(models.Model):
    FUEL = (
        ('G', 'Gasolina'),
        ('E', 'Etanol'),
        ('D', 'Diesel'),
        ('H', 'Hibrido'),
    )

    TYPE = (
        ('M', 'Moto'),
        ('C', 'Carro'),
    )

    type_vehicle = models.CharField(max_length=1, default='M', choices=TYPE, verbose_name='veículo')
    brand_vehicle = models.CharField(max_length=100, verbose_name='marca')
    model_vehicle = models.CharField(max_length=100, verbose_name='modelo')
    year_manufacture_vehicle = models.CharField(max_length=4, verbose_name='ano de fabricação')
    model_year_vehicle = models.CharField(max_length=4, verbose_name='ano do modelo')
    mileage_vehicle = models.FloatField(default=0, verbose_name='quilometragem')
    renavam_vehicle = models.CharField(max_length=11, primary_key=True,
                                       validators=[RENAVAMValidator()], verbose_name='renavam')
    license_plate_vehicle = models.CharField(max_length=7, unique=True, verbose_name='placa')
    chassi_vehicle = models.CharField(max_length=17, unique=True, verbose_name='chassi')
    fuel_vehicle = models.CharField(max_length=1, default='G', choices=FUEL, verbose_name='combustível')
    fuel_tank_vehicle = models.PositiveSmallIntegerField(verbose_name='capacidade do tanque')
    engine_vehicle = models.CharField(max_length=100, verbose_name='motor')
    color_vehicle = models.CharField(max_length=25, verbose_name='cor')
    other_data_vehicle = models.JSONField(blank=True, null=True, verbose_name='mais informações')
    available_vehicle = models.BooleanField(default=True, verbose_name='disponível')
    branch_vehicle = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, verbose_name='filial')
    classification_vehicle = models.ForeignKey(VehicleClassification, on_delete=models.DO_NOTHING,
                                               verbose_name='classificação')
    image_vehicle = models.ImageField(null=True, blank=True, verbose_name='imagem')

    def __str__(self):
        return f'{self.brand_vehicle} / {self.model_vehicle} - {self.model_year_vehicle}'

    def __repr__(self):
        return self.renavam_vehicle

    class Meta:
        verbose_name = 'veículo'

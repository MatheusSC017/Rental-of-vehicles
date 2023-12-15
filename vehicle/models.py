from django.db import models
from django.core.validators import MinValueValidator
from branch.models import Branch
from utils.validators.docbr import RENAVAMValidator


class VehicleClassification(models.Model):
    title = models.CharField(max_length=50, verbose_name='classificação')
    daily_cost = models.FloatField(validators=[MinValueValidator(0)], verbose_name='custo da diária')

    def __str__(self):
        return self.title

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

    type = models.CharField(max_length=1, default='M', choices=TYPE, verbose_name='veículo')
    brand = models.CharField(max_length=100, verbose_name='marca')
    model = models.CharField(max_length=100, verbose_name='modelo')
    year_manufacture = models.PositiveIntegerField(validators=[MinValueValidator(1890)],
                                                           verbose_name='ano de fabricação')
    model_year = models.PositiveIntegerField(validators=[MinValueValidator(1890)], verbose_name='ano do modelo')
    mileage = models.FloatField(default=0, verbose_name='quilometragem')
    renavam = models.CharField(max_length=11, primary_key=True,
                                       validators=[RENAVAMValidator()], verbose_name='renavam')
    license_plate = models.CharField(max_length=7, unique=True, verbose_name='placa')
    chassi = models.CharField(max_length=17, unique=True, verbose_name='chassi')
    fuel = models.CharField(max_length=1, default='G', choices=FUEL, verbose_name='combustível')
    fuel_tank = models.PositiveSmallIntegerField(verbose_name='capacidade do tanque')
    engine = models.CharField(max_length=100, verbose_name='motor')
    color = models.CharField(max_length=25, verbose_name='cor')
    other_data = models.JSONField(blank=True, null=True, verbose_name='mais informações')
    available = models.BooleanField(default=True, verbose_name='disponível')
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, verbose_name='filial')
    classification = models.ForeignKey(VehicleClassification, on_delete=models.DO_NOTHING,
                                               verbose_name='classificação')
    image = models.ImageField(null=True, blank=True, verbose_name='imagem')

    def __str__(self):
        return f'{self.brand} / {self.model} - {self.model_year}'

    def __repr__(self):
        return self.renavam

    class Meta:
        verbose_name = 'veículo'

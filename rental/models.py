from django.db import models
from django.core.validators import MinValueValidator
from branch.models import Branch
from vehicle.models import Vehicle
from staff.models import StaffMember
from client.models import Client


class Insurance(models.Model):
    title_insurance = models.CharField(max_length=100, verbose_name='titulo')
    coverage_insurance = models.JSONField(verbose_name='abrangência')
    price_insurance = models.FloatField(validators=[MinValueValidator(0)], verbose_name='preço')

    class Meta:
        verbose_name = 'seguro'


class Rental(models.Model):
    STATUS = (
        ('A', 'Agendado'),
        ('L', 'Alocado'),
        ('D', 'Devolvido'),
        ('E', 'Devolvido com atraso'),
        ('C', 'Cancelado'),
    )

    vehicle_rental = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING, verbose_name='veículo')
    insurance_rental = models.ForeignKey(Insurance, blank=True, null=True, on_delete=models.DO_NOTHING,
                                         verbose_name='seguro')
    staff_rental = models.ForeignKey(StaffMember, on_delete=models.DO_NOTHING, verbose_name='funcionário')
    client_rental = models.ForeignKey(Client, on_delete=models.DO_NOTHING, related_name='client_rental',
                                      verbose_name='cliente')
    status_rental = models.CharField(max_length=1, choices=STATUS, verbose_name='status')
    outlet_branch_rental = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, verbose_name='filial de saída')
    rent_date_rental = models.DateField(verbose_name='data de alocação')
    devolution_date_rental = models.DateField(verbose_name='data de devolução')
    requested_deadline_rental = models.PositiveSmallIntegerField(verbose_name='prazo requisitado')
    actual_deadline_rental = models.PositiveSmallIntegerField(verbose_name='prazo real')
    fines_rental = models.FloatField(validators=[MinValueValidator(0)], verbose_name='multas')
    rent_deposit_rental = models.FloatField(validators=[MinValueValidator(0)], verbose_name='caução')
    daily_cost_rental = models.FloatField(validators=[MinValueValidator(0)], verbose_name='custo da diária')
    additional_daily_cost_rental = models.FloatField(validators=[MinValueValidator(0)],
                                                     verbose_name='custo adicional da diária')
    return_rate_rental = models.FloatField(validators=[MinValueValidator(0)], verbose_name='taxa de retorno')
    total_cost_rental = models.FloatField(validators=[MinValueValidator(0)], verbose_name='custo total')
    driver_rental = models.ManyToManyField(Client, related_name='driver_rental', verbose_name='condutores')

    class Meta:
        verbose_name = 'aluguel'
        verbose_name_plural = 'alugueis'

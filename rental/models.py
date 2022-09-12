from django.db import models
from django.core.validators import MinValueValidator
from branch.models import Branch
from vehicle.models import Vehicle
from staff.models import StaffMember
from client.models import Client
from .validators import valid_appointment_update_or_cancellation
from datetime import date


class Insurance(models.Model):
    title_insurance = models.CharField(max_length=100, verbose_name='titulo')
    coverage_insurance = models.JSONField(verbose_name='abrangência')
    price_insurance = models.FloatField(validators=[MinValueValidator(0)], verbose_name='preço')

    def __str__(self):
        return self.title_insurance

    class Meta:
        verbose_name = 'seguro'


class Rental(models.Model):
    STATUS = (
        ('A', 'Agendado'),
        ('L', 'Alocado'),
        ('C', 'Cancelado'),
        ('D', 'Devolvido'),
    )

    vehicle_rental = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING, verbose_name='veículo')
    insurance_rental = models.ForeignKey(Insurance, blank=True, null=True, on_delete=models.DO_NOTHING,
                                         verbose_name='seguro')
    staff_rental = models.ForeignKey(StaffMember, on_delete=models.DO_NOTHING, verbose_name='funcionário')
    client_rental = models.ForeignKey(Client, on_delete=models.DO_NOTHING, related_name='client_rental',
                                      verbose_name='cliente')
    status_rental = models.CharField(max_length=1, choices=STATUS, verbose_name='status')
    outlet_branch_rental = models.ForeignKey(Branch, related_name='outlet_branch_rental', on_delete=models.DO_NOTHING,
                                             verbose_name='filial de saída')
    arrival_branch_rental = models.ForeignKey(Branch, null=True, blank=True, related_name='arrival_branch_rental',
                                              on_delete=models.DO_NOTHING, verbose_name='filial de chegada')
    distance_branch_rental = models.PositiveIntegerField(null=True, blank=True, verbose_name='distância entre filiais')
    appointment_date_rental = models.DateField(null=True, blank=True, verbose_name='data de agendamento')
    rent_date_rental = models.DateField(null=True, blank=True, verbose_name='data de alocação')
    devolution_date_rental = models.DateField(null=True, blank=True, verbose_name='data de devolução')
    requested_days_rental = models.PositiveSmallIntegerField(verbose_name='prazo requisitado')
    actual_days_rental = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='prazo real')
    fines_rental = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)], verbose_name='multas')
    rent_deposit_rental = models.FloatField(validators=[MinValueValidator(0)], verbose_name='caução')
    daily_cost_rental = models.FloatField(validators=[MinValueValidator(0)], verbose_name='custo da diária')
    additional_daily_cost_rental = models.FloatField(validators=[MinValueValidator(0)],
                                                     verbose_name='custo adicional da diária')
    return_rate_rental = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)],
                                           verbose_name='taxa de retorno')
    total_cost_rental = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)],
                                          verbose_name='custo total')
    driver_rental = models.ManyToManyField(Client, related_name='driver_rental', verbose_name='condutores')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.status_rental == 'L' and not self.rent_date_rental:
            self.rent_date_rental = date.today()

        if self.status_rental == 'C':
            self.actual_days_rental = 0
            if not valid_appointment_update_or_cancellation(self.appointment_date_rental):
                self.fines_rental = self.calculate_fines()
            self.total_cost_rental = self.fines_rental

        if self.status_rental == 'D':
            # Rate of return value
            self.return_rate_rental = self.distance_branch_rental * 1.2
            # Fine amount for breach of agreement
            self.devolution_date_rental = date.today()
            self.actual_days_rental = self.devolution_date_rental - self.rent_date_rental
            self.fines_rental = self.calculate_fines()
            # Insurance cost
            total_cost_of_insurance = self.insurance_rental.price_insurance * self.actual_days_rental
            # Total cost of rent
            daily_cost_total = self.daily_cost_rental + self.additional_daily_cost_rental
            self.total_cost_rental = (self.actual_days_rental * daily_cost_total) + self.fines_rental \
                                     + self.return_rate_rental + total_cost_of_insurance

        self.save_base()

    def calculate_fines(self):
        daily_cost_total = self.daily_cost_rental + self.additional_daily_cost_rental
        number_of_days = abs(self.actual_days_rental - self.requested_days_rental)
        return round(number_of_days * daily_cost_total * 0.2, 2)

    def __str__(self):
        return f'{self.client_rental} - {self.vehicle_rental}'

    class Meta:
        verbose_name = 'aluguel'
        verbose_name_plural = 'alugueis'

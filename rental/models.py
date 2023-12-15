from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from .validators import valid_appointment_update_or_cancellation
from datetime import datetime, date, timedelta


class Insurance(models.Model):
    title = models.CharField(max_length=100, verbose_name='titulo')
    coverage = models.JSONField(verbose_name='abrangência')
    price = models.FloatField(validators=[MinValueValidator(0)], verbose_name='preço')

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.pk

    class Meta:
        verbose_name = 'seguro'


class AdditionalItems(models.Model):
    name = models.CharField(max_length=50, verbose_name='nome')
    daily_cost = models.FloatField(validators=[MinValueValidator(0)], verbose_name='custo diário')
    stock = models.PositiveSmallIntegerField(default=1, verbose_name='quantidade em estoque')
    branch = models.ForeignKey('branch.Branch', on_delete=models.DO_NOTHING, verbose_name='filial')

    def __str__(self):
        return self.name_additionalitems

    def __repr__(self):
        return self.pk

    class Meta:
        verbose_name = 'item adicional'
        verbose_name_plural = 'itens adicionais'


class Rental(models.Model):
    STATUS = (
        ('A', 'Agendado'),
        ('L', 'Alocado'),
        ('C', 'Cancelado'),
        ('D', 'Devolvido'),
    )

    vehicle = models.ForeignKey('vehicle.Vehicle', on_delete=models.DO_NOTHING, verbose_name='veículo',
                                limit_choices_to={'available': True})
    insurance = models.ForeignKey(Insurance, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name='seguro')
    staff = models.ForeignKey('staff.StaffMember', on_delete=models.DO_NOTHING, verbose_name='funcionário')
    client = models.ForeignKey('client.Client', on_delete=models.DO_NOTHING, related_name='client',
                               verbose_name='cliente')
    status = models.CharField(max_length=1, choices=STATUS, verbose_name='status')
    outlet_branch = models.ForeignKey('branch.Branch', related_name='outlet_branch', on_delete=models.DO_NOTHING,
                                      verbose_name='filial de saída')
    arrival_branch = models.ForeignKey('branch.Branch', null=True, blank=True, related_name='arrival_branch',
                                       on_delete=models.DO_NOTHING, verbose_name='filial de chegada')
    distance_branch = models.PositiveIntegerField(null=True, blank=True, verbose_name='distância entre filiais')
    appointment_date = models.DateField(null=True, blank=True, verbose_name='data de agendamento')
    rent_date = models.DateField(null=True, blank=True, verbose_name='data de alocação')
    devolution_date = models.DateField(null=True, blank=True, verbose_name='data de devolução')
    requested_days = models.PositiveSmallIntegerField(verbose_name='prazo requisitado')
    actual_days = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='prazo real')
    fines = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)], verbose_name='multas')
    rent_deposit = models.FloatField(validators=[MinValueValidator(0)], verbose_name='caução')
    daily_cost = models.FloatField(validators=[MinValueValidator(0)], verbose_name='custo da diária')
    additional_daily_cost = models.FloatField(validators=[MinValueValidator(0)],
                                              verbose_name='custo adicional da diária')
    return_rate = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)],
                                    verbose_name='taxa de retorno')
    total_cost = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)],
                                   verbose_name='custo total')
    driver = models.ManyToManyField('client.Client', related_name='driver', verbose_name='condutores')

    def save(self, *args, **kwargs):
        if self.status == 'L' and not self.rent_date:
            self.rent_date = date.today()

        if self.status == 'C':
            self.actual_days = 0
            if not valid_appointment_update_or_cancellation(self.appointment_date):
                self.fines = self.calculate_fines()
            self.total_cost = self.fines

        if self.status == 'D':
            # Set arrival branch if it is None
            if self.arrival_branch is None:
                self.arrival_branch = self.outlet_branch
            # Rate of return value
            self.return_rate = self.distance_branch * 1.2 if self.distance_branch else 0.
            # Fine amount for breach of agreement
            self.devolution_date = date.today()
            self.actual_days = (self.devolution_date - self.rent_date).days + 1
            self.fines = self.calculate_fines()
            # Insurance cost
            total_cost_of_insurance = self.insurance.price * self.actual_days \
                if self.insurance else 0.
            # Total cost of rent
            daily_cost_total = self.daily_cost + self.additional_daily_cost
            total_cost = self.actual_days * daily_cost_total
            self.total_cost = sum([total_cost, self.fines, self.return_rate, total_cost_of_insurance])
        super(Rental, self).save(*args, **kwargs)

    def calculate_fines(self):
        daily_cost_total = self.daily_cost + self.additional_daily_cost

        if self.status == 'C':
            number_of_days = self.requested_days
        else:
            number_of_days = 0
            if self.appointment_date:
                number_of_days += abs((self.appointment_date - self.rent_date).days)
                initial_date = self.appointment_date
            else:
                initial_date = self.rent_date
            expected_return_date = initial_date + timedelta(days=self.requested_days - 1)
            number_of_days += abs((self.devolution_date - expected_return_date).days)

        return round(number_of_days * daily_cost_total * 0.2, 2)

    def __str__(self):
        return f'{self.client} - {self.vehicle}'

    class Meta:
        verbose_name = 'aluguel'
        verbose_name_plural = 'alugueis'


class RentalAdditionalItem(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, verbose_name='Aluguel',
                               related_name='additional_items')
    additional_item = models.ForeignKey(AdditionalItems, on_delete=models.CASCADE, verbose_name='Item adicional')
    number = models.PositiveSmallIntegerField(default=1, verbose_name='Número de itens')

    class Meta:
        unique_together = [['rental', 'additional_item']]

    def __str__(self):
        return f'{self.additional_item}: {self.number}'

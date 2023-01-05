from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from .validators import valid_appointment_update_or_cancellation
from datetime import datetime, date, timedelta


class Insurance(models.Model):
    title_insurance = models.CharField(max_length=100, verbose_name='titulo')
    coverage_insurance = models.JSONField(verbose_name='abrangência')
    price_insurance = models.FloatField(validators=[MinValueValidator(0)], verbose_name='preço')

    def __str__(self):
        return self.title_insurance

    def __repr__(self):
        return self.pk

    class Meta:
        verbose_name = 'seguro'


class AdditionalItems(models.Model):
    name_additionalitems = models.CharField(max_length=50, verbose_name='nome')
    daily_cost_additionalitems = models.FloatField(validators=[MinValueValidator(0)], verbose_name='custo diário')
    stock_additionalitems = models.PositiveSmallIntegerField(default=1, verbose_name='quantidade em estoque')
    branch_additionalitems = models.ForeignKey('branch.Branch', on_delete=models.DO_NOTHING, verbose_name='filial')

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

    vehicle_rental = models.ForeignKey('vehicle.Vehicle', on_delete=models.DO_NOTHING, verbose_name='veículo',
                                       limit_choices_to={'available_vehicle': True})
    insurance_rental = models.ForeignKey(Insurance, blank=True, null=True, on_delete=models.DO_NOTHING,
                                         verbose_name='seguro')
    staff_rental = models.ForeignKey('staff.StaffMember', on_delete=models.DO_NOTHING, verbose_name='funcionário')
    client_rental = models.ForeignKey('client.Client', on_delete=models.DO_NOTHING, related_name='client_rental',
                                      verbose_name='cliente')
    status_rental = models.CharField(max_length=1, choices=STATUS, verbose_name='status')
    outlet_branch_rental = models.ForeignKey('branch.Branch', related_name='outlet_branch_rental',
                                             on_delete=models.DO_NOTHING, verbose_name='filial de saída')
    arrival_branch_rental = models.ForeignKey('branch.Branch', null=True, blank=True,
                                              related_name='arrival_branch_rental', on_delete=models.DO_NOTHING,
                                              verbose_name='filial de chegada')
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
    driver_rental = models.ManyToManyField('client.Client', related_name='driver_rental', verbose_name='condutores')

    def save(self, *args, **kwargs):
        if self.status_rental == 'L' and not self.rent_date_rental:
            self.rent_date_rental = date.today()

        if self.status_rental == 'C':
            self.actual_days_rental = 0
            if not valid_appointment_update_or_cancellation(self.appointment_date_rental):
                self.fines_rental = self.calculate_fines()
            self.total_cost_rental = self.fines_rental

        if self.status_rental == 'D':
            # Set arrival branch if it is None
            if self.arrival_branch_rental is None:
                self.arrival_branch_rental = self.outlet_branch_rental
            # Rate of return value
            self.return_rate_rental = self.distance_branch_rental * 1.2 if self.distance_branch_rental else 0.
            # Fine amount for breach of agreement
            self.devolution_date_rental = date.today()
            self.actual_days_rental = (self.devolution_date_rental - self.rent_date_rental).days + 1
            self.fines_rental = self.calculate_fines()
            # Insurance cost
            total_cost_of_insurance = self.insurance_rental.price_insurance * self.actual_days_rental \
                if self.insurance_rental else 0.
            # Total cost of rent
            daily_cost_total = self.daily_cost_rental + self.additional_daily_cost_rental
            total_cost = self.actual_days_rental * daily_cost_total
            self.total_cost_rental = sum([total_cost, self.fines_rental,
                                          self.return_rate_rental, total_cost_of_insurance])
        super(Rental, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.status_rental == 'A':
            self.devolution_date_expected_rental = str(timezone.make_aware(
                datetime.strptime(str(self.appointment_date_rental), '%Y-%m-%d')
            ) + timezone.timedelta(days=self.requested_days_rental))[:10]

        if self.status_rental == 'L':
            self.devolution_date_expected_rental = str(timezone.now() +
                                                       timezone.timedelta(days=self.requested_days_rental))[:10]

    def calculate_fines(self):
        daily_cost_total = self.daily_cost_rental + self.additional_daily_cost_rental

        if self.status_rental == 'C':
            number_of_days = self.requested_days_rental
        else:
            number_of_days = 0
            if self.appointment_date_rental:
                number_of_days += abs((self.appointment_date_rental - self.rent_date_rental).days)
                initial_date = self.appointment_date_rental
            else:
                initial_date = self.rent_date_rental
            expected_return_date = initial_date + timedelta(days=self.requested_days_rental - 1)
            number_of_days += abs((self.devolution_date_rental - expected_return_date).days)

        return round(number_of_days * daily_cost_total * 0.2, 2)

    def __str__(self):
        return f'{self.client_rental} - {self.vehicle_rental}'

    class Meta:
        verbose_name = 'aluguel'
        verbose_name_plural = 'alugueis'


class RentalAdditionalItem(models.Model):
    rental_relationship = models.ForeignKey(Rental, on_delete=models.CASCADE, verbose_name='Aluguel',
                                            related_name='additional_items_rental')
    additional_item_relationship = models.ForeignKey(AdditionalItems, on_delete=models.CASCADE,
                                                     verbose_name='Item adicional')
    number_relationship = models.PositiveSmallIntegerField(default=1, verbose_name='Número de itens')

    class Meta:
        unique_together = [['rental_relationship', 'additional_item_relationship']]

    def __str__(self):
        return f'{self.additional_item_relationship}: {self.number_relationship}'

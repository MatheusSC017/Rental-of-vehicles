from django.db import models
from address.models import Address


class Branch(models.Model):
    opening_hours_start = models.TimeField(verbose_name='início do horário de funcionamento')
    opening_hours_end = models.TimeField(verbose_name='fim do horário de funcionamento')
    address_branch = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name='endereço')

    class Meta:
        verbose_name = 'filial'
        verbose_name_plural = 'filiais'

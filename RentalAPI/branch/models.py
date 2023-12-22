from django.db import models
from address.models import Address


class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name='nome')
    opening_hours_start = models.TimeField(verbose_name='início do horário de funcionamento')
    opening_hours_end = models.TimeField(verbose_name='fim do horário de funcionamento')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name='endereço')

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.pk)

    def address_info(self):
        return str(self.address)

    class Meta:
        verbose_name = 'filial'
        verbose_name_plural = 'filiais'

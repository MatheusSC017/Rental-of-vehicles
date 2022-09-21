from django.db import models
from address.models import Address


class Branch(models.Model):
    name_branch = models.CharField(max_length=100, verbose_name='nome')
    opening_hours_start_branch = models.TimeField(verbose_name='início do horário de funcionamento')
    opening_hours_end_branch = models.TimeField(verbose_name='fim do horário de funcionamento')
    address_branch = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name='endereço')

    def __str__(self):
        return self.name_branch

    def address_info(self):
        return str(self.address_branch)

    class Meta:
        verbose_name = 'filial'
        verbose_name_plural = 'filiais'

from django.db import models
from address.models import Address
from utils.models.managers import ActiveObjectsManager


class Branch(models.Model):
    name = models.CharField(max_length=100, null=False, verbose_name='nome')
    opening_hours_start = models.TimeField(null=False, verbose_name='início do horário de funcionamento')
    opening_hours_end = models.TimeField(null=False, verbose_name='fim do horário de funcionamento')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=False, verbose_name='endereço')
    is_active = models.BooleanField(default=True)

    objects = ActiveObjectsManager()

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.pk)

    def address_info(self):
        return str(self.address)

    class Meta:
        verbose_name = 'filial'
        verbose_name_plural = 'filiais'

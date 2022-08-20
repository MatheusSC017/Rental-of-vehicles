from django.db import models


class Address(models.Model):
    cep_address = models.CharField(max_length=8, verbose_name='CEP')
    state_address = models.CharField(max_length=2, verbose_name='estado (sigla)')
    city_address = models.CharField(max_length=100, verbose_name='cidade')
    district_address = models.CharField(max_length=100, verbose_name='bairro')
    street_address = models.CharField(max_length=100, verbose_name='rua')
    number_address = models.CharField(max_length=30, verbose_name='número')

from django.db import models
from django.contrib.auth.models import User
from address.models import Address


class Client(models.Model):
    GENDER = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('N', 'Não desejo me identificar'),
    )

    user_client = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário')
    cpf_client = models.CharField(max_length=11, primary_key=True, verbose_name='CPF')
    rg_client = models.CharField(max_length=20, verbose_name='RG')
    cnh_client = models.CharField(max_length=11, unique=True, verbose_name='CNH')
    gender_client = models.CharField(max_length=1, choices=GENDER, verbose_name='sexo')
    age_client = models.PositiveSmallIntegerField(verbose_name='idade')
    finance_client = models.FloatField(verbose_name='renda')
    phone_client = models.CharField(max_length=20, verbose_name='telefone')
    address_client = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name='endereço')

    def __str__(self):
        return f'{self.user_client.first_name} {self.user_client.last_name}'

    class Meta:
        verbose_name = 'cliente'

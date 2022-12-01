from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from address.models import Address
from utils.validators.docbr import CPFValidator, CNHValidator
from utils.validators.basic_user import PhoneValidator


class Person(models.Model):
    GENDER = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('N', 'Não desejo me identificar'),
    )

    cpf_person = models.CharField(max_length=11, primary_key=True, validators=[CPFValidator()], verbose_name='CPF')
    rg_person = models.CharField(max_length=20, verbose_name='RG')
    gender_person = models.CharField(max_length=1, choices=GENDER, verbose_name='sexo')
    age_person = models.PositiveSmallIntegerField(validators=[MinValueValidator(18)], verbose_name='idade')
    phone_person = models.CharField(max_length=16, validators=[PhoneValidator()], verbose_name='telefone')
    address_person = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name='endereço')

    class Meta:
        abstract = True


class Client(Person):
    user_client = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário')
    cnh_client = models.CharField(max_length=11, unique=True, null=True, validators=[CNHValidator()], verbose_name='CNH')
    finance_client = models.FloatField(verbose_name='renda')

    def __str__(self):
        return f'{self.user_client.first_name} {self.user_client.last_name}'

    def __repr__(self):
        return self.cpf_person

    class Meta:
        verbose_name = 'cliente'

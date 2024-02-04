from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from address.models import Address
from utils.validators.docbr import CPFValidator, CNHValidator
from utils.validators.basic_user import PhoneValidator
from utils.models.managers import ActiveObjectsManager


class Person(models.Model):
    GENDER = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('N', 'Não desejo me identificar'),
    )

    cpf = models.CharField(max_length=11, primary_key=True, validators=[CPFValidator()], verbose_name='CPF')
    rg = models.CharField(max_length=20, verbose_name='RG')
    gender = models.CharField(max_length=1, choices=GENDER, verbose_name='sexo')
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18)], verbose_name='idade')
    phone = models.CharField(max_length=16, validators=[PhoneValidator()], verbose_name='telefone')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name='endereço')

    class Meta:
        abstract = True


class Client(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário')
    cnh = models.CharField(max_length=11, unique=True, null=True, validators=[CNHValidator()], verbose_name='CNH')
    finance = models.FloatField(verbose_name='renda')
    is_active = models.BooleanField(default=True)

    objects = ActiveObjectsManager()

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __repr__(self):
        return str(self.cpf)

    class Meta:
        verbose_name = 'cliente'

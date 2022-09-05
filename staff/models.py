from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from client.models import Person
from branch.models import Branch


class StaffMember(Person):
    user_staffmember = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário')
    salary_staffmember = models.FloatField(validators=[MinValueValidator(0)], verbose_name='salário')
    branch_staffmember = models.ForeignKey(Branch, null=True, on_delete=models.SET_NULL, verbose_name='filial')

    def __str__(self):
        return f'{self.user_staffmember.first_name} {self.user_staffmember.last_name}'

    class Meta:
        verbose_name = 'membro da equipe'
        verbose_name_plural = 'membros da equipe'

from django.db import models
from django.contrib.auth.models import User, ContentType, Permission
from django.core.validators import MinValueValidator
from client.models import Person
from address.models import Address
from branch.models import Branch
from client.models import Client
from vehicle.models import Vehicle, VehicleClassification
import rental


class StaffMember(Person):
    user_staffmember = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário')
    salary_staffmember = models.FloatField(validators=[MinValueValidator(0)], verbose_name='salário')
    branch_staffmember = models.ForeignKey(Branch, null=True, on_delete=models.SET_NULL, verbose_name='filial')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        model_classes = [Address, Branch, Client, rental.models.Insurance, rental.models.Rental,
                         Vehicle, VehicleClassification, User, ]
        for model_class in model_classes:
            content_type = ContentType.objects.get_for_model(model_class)
            permissions = Permission.objects.filter(content_type=content_type)
            for perm in permissions:
                self.user_staffmember.user_permissions.add(perm)

    def __str__(self):
        return f'{self.user_staffmember.first_name} {self.user_staffmember.last_name}'

    class Meta:
        verbose_name = 'membro da equipe'
        verbose_name_plural = 'membros da equipe'

import rental
from django.db import models
from django.contrib.auth.models import User, ContentType, Permission
from django.core.validators import MinValueValidator
from client.models import Person, Client
from address.models import Address
from branch.models import Branch
from vehicle.models import Vehicle, VehicleClassification


class StaffMember(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário')
    salary = models.FloatField(validators=[MinValueValidator(0)], verbose_name='salário')
    branch = models.ForeignKey(Branch, null=True, on_delete=models.SET_NULL, verbose_name='filial')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        model_classes = [Address, Branch, Client, rental.models.Rental, rental.models.Insurance,
                         rental.models.AdditionalItems, Vehicle, VehicleClassification, User, ]
        for model_class in model_classes:
            content_type = ContentType.objects.get_for_model(model_class)
            permissions = Permission.objects.filter(content_type=content_type)
            for perm in permissions:
                self.user.user_permissions.add(perm)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __repr__(self):
        return str(self.cpf)

    class Meta:
        verbose_name = 'membro da equipe'
        verbose_name_plural = 'membros da equipe'

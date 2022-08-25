from django.db import models


class Address(models.Model):
    STATES = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    )

    cep_address = models.CharField(max_length=9, verbose_name='CEP')
    state_address = models.CharField(max_length=2, choices=STATES, verbose_name='estado')
    city_address = models.CharField(max_length=100, verbose_name='cidade')
    district_address = models.CharField(max_length=100, verbose_name='bairro')
    street_address = models.CharField(max_length=100, verbose_name='rua')
    number_address = models.CharField(max_length=30, verbose_name='número')

    def __str__(self):
        return f'{self.street_address} - {self.number_address}, ' \
               f'{self.district_address}, {self.city_address}/ {self.state_address}'

    class Meta:
        verbose_name = 'endereço'

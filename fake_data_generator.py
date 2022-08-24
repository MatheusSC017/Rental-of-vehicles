import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from faker import Faker
from random import choices, randrange
from address.models import Address

fake = Faker()

STATES = ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA',
          'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO')


def address_generator():
    cep = randrange(10000000, 99999999)
    state = choices(STATES)
    city = fake.city()
    district = fake.street_suffix()
    street = fake.street_name()
    number = fake.building_number()

    Address.objects.create(cep_address=cep,
                           state_address=state,
                           city_address=city,
                           district_address=district,
                           street_address=street,
                           number_address=number)


if __name__ == '__main__':
    for _ in range(20):
        address_generator()

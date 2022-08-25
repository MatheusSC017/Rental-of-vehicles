import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

import faker
from random import randrange, choice
from address.models import Address
from client.models import Client
from django.contrib.auth.models import User

fake = faker.Faker('pt_BR')


def address_generator():
    cep = fake.postcode()
    state = fake.estado_sigla()
    city = fake.city()
    district = fake.bairro()
    street = fake.street_name()
    number = fake.building_number()

    address = Address.objects.create(
        cep_address=cep,
        state_address=state,
        city_address=city,
        district_address=district,
        street_address=street,
        number_address=number
    )

    return address


def user_generator():
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = first_name + str(randrange(10000, 99999))
    email = username + '@email.com.br'
    password = username
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    return user


def client_generator():
    gender_options = ('M', 'F', 'N')

    user = user_generator()
    cpf = fake.cpf()
    rg = fake.rg()
    cnh = randrange(11111111111, 99999999999)
    gender = choice(gender_options)
    age = randrange(18, 99)
    finance = randrange(500, 30000)
    phone = fake.cellphone_number()
    address = address_generator()

    client = Client.objects.create(
        user_client=user,
        cpf_client=cpf,
        rg_client=rg,
        cnh_client=cnh,
        gender_client=gender,
        age_client=age,
        finance_client=finance,
        phone_client=phone,
        address_client=address
    )

    return client


if __name__ == '__main__':
    for _ in range(50):
        client_generator()

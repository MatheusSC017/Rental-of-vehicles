import os
import json
from random import randrange, choice, choices
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

import faker
from unidecode import unidecode
from validate_docbr import CPF, CNH, RENAVAM
from django.contrib.auth.models import User
from address.models import Address
from client.models import Client
from branch.models import Branch
from vehicle.models import Vehicle, VehicleClassification
from rental.models import Insurance, AdditionalItems

fake = faker.Faker('pt_BR')
cpf_generator = CPF()
cnh_generator = CNH()
renavam_generator = RENAVAM()


def address_generator():
    cep = fake.postcode()
    state = fake.estado_sigla()
    city = fake.city()
    district = fake.bairro()
    street = fake.street_name()
    number = fake.building_number()

    address = Address.objects.create(
        cep=cep,
        state=state,
        city=city,
        district=district,
        street=street,
        number=number
    )

    return address


def user_generator():
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = first_name.replace(' ', '_') + str(randrange(10000, 99999))
    email = unidecode(username + '@email.com.br')
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
    cpf = cpf_generator.generate()
    rg = fake.rg()
    cnh = cnh_generator.generate()
    gender = choice(gender_options)
    age = randrange(18, 99)
    finance = randrange(500, 30000)
    phone = fake.cellphone_number()[4:]
    address = address_generator()

    client = Client.objects.create(
        user=user,
        cpf=cpf,
        rg=rg,
        cnh=cnh,
        gender=gender,
        age=age,
        finance=finance,
        phone=phone,
        address=address
    )

    return client


def branch_generator():
    name = fake.street_name()
    start = randrange(5, 13)
    opening_hours_start = str(start) + ':00:00'
    opening_hours_end = str(start + 8) + ':00:00'
    address = address_generator()

    branch = Branch.objects.create(
        name=name,
        opening_hours_start=opening_hours_start,
        opening_hours_end=opening_hours_end,
        address=address
    )

    return branch


def classification_generator():
    title = ' '.join(fake.words(nb=3))
    daily_cost = randrange(500, 5000) / 100

    classification = VehicleClassification.objects.create(
        title=title,
        daily_cost=daily_cost
    )

    return classification


def vehicle_generator(branches, classifications):
    def json_generator():
        data = {}
        for _ in range(randrange(0, 5)):
            data[fake.words(nb=1)[0]] = ' '.join(fake.words(nb=2))
        return json.dumps(data)

    year_manufacture = randrange(1960, 2017)

    vehicle = Vehicle.objects.create(
        type=choice('MC'),
        brand=' '.join(fake.words(nb=1)),
        model=' '.join(fake.words(nb=2)),
        year_manufacture=year_manufacture,
        model_year=year_manufacture + randrange(0, 5),
        mileage=float(randrange(0, 2000)),
        renavam=renavam_generator.generate(),
        license_plate=fake.license_plate().replace('-', ''),
        chassi=str(randrange(11111111111111111, 99999999999999999)),
        fuel=choice('GEDH'),
        fuel_tank=randrange(15, 50),
        engine=' '.join(fake.words()),
        color=fake.color_name(),
        other_data=json_generator(),
        available=choices([True, False], weights=(90, 10))[0],
        branch=choice(branches),
        classification=choice(classifications)
    )

    return vehicle


def insurance_generator():
    def json_generator():
        data = {}
        for _ in range(randrange(3, 7)):
            data[fake.words(nb=1)[0]] = f'R$ {randrange(1000, 1000000):.2f}'
        return json.dumps(data)

    title = ' '.join(fake.words(nb=3))
    coverage = json_generator()
    price = randrange(100, 2000) / 100

    Insurance.objects.create(
        title=title,
        coverage=coverage,
        price=price
    )


def additional_item_generator(branches):
    name = ' '.join(fake.words(nb=3))
    daily_cost = randrange(10, 500) / 100
    stock = randrange(1, 15)

    AdditionalItems.objects.create(
        name=name,
        daily_cost=daily_cost,
        branch=choice(branches),
        stock=stock
    )


if __name__ == '__main__':
    for _ in range(500):
        client_generator()

    branches_list = []
    for _ in range(30):
        branches_list.append(branch_generator())

    classifications_list = []
    for _ in range(5):
        classifications_list.append(classification_generator())

    for _ in range(150):
        vehicle_generator(branches_list, classifications_list)

    for _ in range(10):
        insurance_generator()

    for _ in range(100):
        additional_item_generator(branches_list)

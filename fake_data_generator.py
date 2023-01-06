import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

import faker
import json
from validate_docbr import CPF, CNH, RENAVAM
from random import randrange, choice, choices
from address.models import Address
from client.models import Client
from branch.models import Branch
from vehicle.models import Vehicle, VehicleClassification
from rental.models import Insurance, AdditionalItems
from django.contrib.auth.models import User
from unidecode import unidecode

fake = faker.Faker('pt_BR')
cpf = CPF()
cnh = CNH()
renavam = RENAVAM()


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
    cpf_client = cpf.generate()
    rg = fake.rg()
    cnh_client = cnh.generate()
    gender = choice(gender_options)
    age = randrange(18, 99)
    finance = randrange(500, 30000)
    phone = fake.cellphone_number()[4:]
    address = address_generator()

    client = Client.objects.create(
        user_client=user,
        cpf_person=cpf_client,
        rg_person=rg,
        cnh_client=cnh_client,
        gender_person=gender,
        age_person=age,
        finance_client=finance,
        phone_person=phone,
        address_person=address
    )

    return client


def branch_generator():
    name_branch = fake.street_name()
    start = randrange(5, 13)
    opening_hours_start = str(start) + ':00:00'
    opening_hours_end = str(start + 8) + ':00:00'
    address = address_generator()

    branch = Branch.objects.create(
        name_branch=name_branch,
        opening_hours_start_branch=opening_hours_start,
        opening_hours_end_branch=opening_hours_end,
        address_branch=address
    )

    return branch


def classification_generator():
    title = ' '.join(fake.words(nb=3))
    daily_cost = randrange(500, 5000) / 100

    classification = VehicleClassification.objects.create(
        title_classification=title,
        daily_cost_classification=daily_cost
    )

    return classification


def vehicle_generator(branches, classifications):
    def json_generator():
        data = dict()
        for _ in range(randrange(0, 5)):
            data[fake.words(nb=1)[0]] = ' '.join(fake.words(nb=2))
        return json.dumps(data)

    type_vehicle = choice('MC')
    brand = ' '.join(fake.words(nb=1))
    model = ' '.join(fake.words(nb=2))
    year_manufacture = randrange(1960, 2017)
    model_year = year_manufacture + randrange(0, 5)
    mileage = float(randrange(0, 2000))
    renavam_vehicle = renavam.generate()
    license_plate = fake.license_plate().replace('-', '')
    chassi = str(randrange(11111111111111111, 99999999999999999))
    fuel = choice('GEDH')
    fuel_tank = randrange(15, 50)
    engine = ' '.join(fake.words())
    color = fake.color_name()
    other_data = json_generator()
    available = choices([True, False], weights=(90, 10))[0]
    branch = choice(branches)
    classification = choice(classifications)

    vehicle = Vehicle.objects.create(
        type_vehicle=type_vehicle,
        brand_vehicle=brand,
        model_vehicle=model,
        year_manufacture_vehicle=year_manufacture,
        model_year_vehicle=model_year,
        mileage_vehicle=mileage,
        renavam_vehicle=renavam_vehicle,
        license_plate_vehicle=license_plate,
        chassi_vehicle=chassi,
        fuel_vehicle=fuel,
        fuel_tank_vehicle=fuel_tank,
        engine_vehicle=engine,
        color_vehicle=color,
        other_data_vehicle=other_data,
        available_vehicle=available,
        branch_vehicle=branch,
        classification_vehicle=classification
    )

    return vehicle


def insurance_generator():
    def json_generator():
        data = dict()
        for _ in range(randrange(3, 7)):
            data[fake.words(nb=1)[0]] = f'R$ {randrange(1000, 1000000):.2f}'
        return json.dumps(data)

    title = ' '.join(fake.words(nb=3))
    coverage = json_generator()
    price = randrange(100, 2000) / 100

    Insurance.objects.create(
        title_insurance=title,
        coverage_insurance=coverage,
        price_insurance=price
    )


def additional_item_generator(branches):
    name = ' '.join(fake.words(nb=3))
    daily_cost = randrange(10, 500) / 100
    stock = randrange(1, 15)

    AdditionalItems.objects.create(
        name_additionalitems=name,
        daily_cost_additionalitems=daily_cost,
        branch_additionalitems=choice(branches),
        stock_additionalitems=stock

    )


if __name__ == '__main__':
    for _ in range(500):
        client_generator()

    branches_list = list()
    for _ in range(30):
        branches_list.append(branch_generator())

    classifications_list = list()
    for _ in range(5):
        classifications_list.append(classification_generator())

    for _ in range(150):
        vehicle_generator(branches_list, classifications_list)

    for _ in range(10):
        insurance_generator()

    for _ in range(100):
        additional_item_generator(branches_list)

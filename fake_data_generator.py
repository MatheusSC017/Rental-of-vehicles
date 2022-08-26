import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

import faker
from random import randrange, choice
from address.models import Address
from client.models import Client
from branch.models import Branch
from vehicle.models import Vehicle
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


def vehicle_generator(branches):
    type = choice('MC')
    brand = ' '.join(fake.words(nb=1))
    model = ' '.join(fake.words(nb=2))
    year_manufacture = randrange(1960, 2020)
    model_year = year_manufacture + randrange(0, 5)
    mileage = float(randrange(0, 2000))
    license_plate = fake.license_plate()
    chassi = str(randrange(11111111111111111, 99999999999999999))
    fuel = choice('GEDH')
    fuel_tank = randrange(15, 50)
    engine = ' '.join(fake.words())
    color = fake.color_name()
    other_data = fake.sentence()
    branch = choice(branches)

    vehicle = Vehicle.objects.create(
        type_vehicle=type,
        brand_vehicle=brand,
        model_vehicle=model,
        year_manufacture_vehicle=year_manufacture,
        model_year_vehicle=model_year,
        mileage_vehicle=mileage,
        license_plate_vehicle=license_plate,
        chassi_vehicle=chassi,
        fuel_vehicle=fuel,
        fuel_tank_vehicle=fuel_tank,
        engine_vehicle=engine,
        color_vehicle=color,
        other_data_vehicle=other_data,
        branch_vehicle=branch
    )

    return vehicle


if __name__ == '__main__':
    '''
    for _ in range(50):
        client_generator()
    '''
    braches = list()
    for _ in range(10):
        braches.append(branch_generator())

    for _ in range(50):
        vehicle_generator(braches)

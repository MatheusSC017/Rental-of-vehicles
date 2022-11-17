from django.test import TestCase
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from address.models import Address
from client.models import Client
from staff.models import StaffMember
from branch.models import Branch
from vehicle.models import Vehicle, VehicleClassification
from .models import Rental, Insurance, AdditionalItems
from . import validators
from random import choice, choices, randrange
from validate_docbr import CPF, CNH, RENAVAM
import faker
import json


class ValidationsTestCase(TestCase):
    def setUp(self) -> None:
        self.allow_field_update = {
            'A': ('vehicle_rental', 'insurance_rental', 'status_rental', 'appointment_date_rental',
                  'requested_days_rental', 'rent_deposit_rental', 'additional_daily_cost_rental',
                  'driver_rental',),
            'L': ('status_rental', 'driver_rental',),
            'C': ('status_rental',),
            'D': ('status_rental', 'arrival_branch_rental', 'distance_branch_rental',),
        }

        fake = faker.Faker('pt_BR')
        cpf = CPF()
        cnh = CNH()
        renavam = RENAVAM()

        def json_generator():
            data = dict()
            for _ in range(randrange(3, 8)):
                data[fake.words(nb=1)[0]] = ' '.join(fake.words(nb=2))
            return json.dumps(data)

        username = [fake.first_name() + str(randrange(10000, 99999)) for _ in range(2)]
        users = [User.objects.create_user(
            username=username[i],
            email=username[i] + '@email.com.br',
            password=username[i]) for i in range(2)]

        addresses = [Address.objects.create(
            cep_address=fake.postcode(),
            state_address=fake.estado_sigla(),
            city_address=fake.city(),
            district_address=fake.bairro(),
            street_address=fake.street_name(),
            number_address=fake.building_number()
        ) for _ in range(3)]

        client = Client.objects.create(
            user_client=users[0],
            cpf_person=cpf.generate(),
            rg_person=fake.rg(),
            cnh_client=cnh.generate(),
            gender_person=choice(('M', 'F', 'N')),
            age_person=randrange(18, 99),
            finance_client=randrange(500, 30000),
            phone_person=fake.cellphone_number()[4:],
            address_person=addresses[0]
        )

        branches = [Branch.objects.create(
            name_branch=fake.street_name(),
            opening_hours_start_branch=str(randrange(5, 13)) + ':00:00',
            opening_hours_end_branch=str(randrange(5, 13) + 8) + ':00:00',
            address_branch=addresses[1]
        ) for _ in range(2)]

        staffmember = StaffMember.objects.create(
            user_staffmember=users[0],
            cpf_person=cpf.generate(),
            rg_person=fake.rg(),
            gender_person=choice(('M', 'F', 'N')),
            age_person=randrange(18, 99),
            salary_staffmember=randrange(500, 30000),
            phone_person=fake.cellphone_number()[4:],
            address_person=addresses[2],
            branch_staffmember=branches[0]
        )

        classification = VehicleClassification.objects.create(
            title_classification=' '.join(fake.words(nb=3)),
            daily_cost_classification=randrange(500, 5000) / 100
        )

        year_manufacture = randrange(1960, 2020)
        vehicle = Vehicle.objects.create(
            type_vehicle=choice('MC'),
            brand_vehicle=' '.join(fake.words(nb=1)),
            model_vehicle=' '.join(fake.words(nb=2)),
            year_manufacture_vehicle=year_manufacture,
            model_year_vehicle=year_manufacture + randrange(0, 5),
            mileage_vehicle=float(randrange(0, 2000)),
            renavam_vehicle=renavam.generate(),
            license_plate_vehicle=fake.license_plate().replace('-', ''),
            chassi_vehicle=str(randrange(11111111111111111, 99999999999999999)),
            fuel_vehicle=choice('GEDH'),
            fuel_tank_vehicle=randrange(15, 50),
            engine_vehicle=' '.join(fake.words()),
            color_vehicle=fake.color_name(),
            other_data_vehicle=json_generator(),
            available_vehicle=choices([True, False], weights=(90, 10))[0],
            branch_vehicle=branches[0],
            classification_vehicle=classification
        )

        insurance = Insurance.objects.create(
            title_insurance=' '.join(fake.words(nb=2)),
            coverage_insurance=json_generator(),
            price_insurance=randrange(100, 2000) / 100
        )

        additional_items = [AdditionalItems.objects.create(
            name_additionalitems=' '.join(fake.words(nb=2)),
            daily_cost_additionalitems=randrange(50, 500) / 100
        ) for _ in range(2)]

        self.rental = Rental.objects.create(
            vehicle_rental=vehicle,
            insurance_rental=insurance,
            staff_rental=staffmember,
            client_rental=client,
            status_rental='A',
            outlet_branch_rental=branches[0],
            arrival_branch_rental=branches[1],
            distance_branch_rental=randrange(0, 5000),
            appointment_date_rental=timezone.now(),
            rent_date_rental=timezone.now(),
            devolution_date_rental=timezone.now() + timezone.timedelta(days=randrange(1, 5)),
            requested_days_rental=randrange(1, 5),
            actual_days_rental=randrange(1, 5),
            rent_deposit_rental=randrange(100, 500),
            daily_cost_rental=randrange(500, 5000) / 100,
            additional_daily_cost_rental=randrange(50, 500) / 100,
        )

    def test_initial_state_value_of_rental(self) -> None:
        initial_values = ['A', 'L', 'C', 'D']
        output_values = list()
        for inital_value in initial_values:
            output_values.append(validators.valid_rental_states_on_create(inital_value))
        self.assertEqual(output_values, [True, True, False, False])

    def test_update_state_value_of_rental(self) -> None:
        old_values = new_values = ['A', 'L', 'C', 'D']
        expected_output_values = [
            [True, True, True, False],
            [False, True, False, True],
            [False, False, False, False],
            [False, False, False, False],
        ]
        for i, old_value in enumerate(old_values):
            output_values = [validators.valid_rental_states_on_update(old_value, new_value) for new_value in new_values]
            self.assertEqual(output_values, expected_output_values[i])

    def test_appointament_update_or_cancelation(self) -> None:
        today = date.today()
        entry_dates = [
            today + timedelta(days=5),
            today + timedelta(days=3),
            today,
            today - timedelta(days=3),
            today - timedelta(days=5),
        ]

        expected_response = [True, False, False, False, False]

        for entry, response in zip(entry_dates, expected_response):
            self.assertEqual(validators.valid_appointment_update_or_cancellation(entry), response)

    def test_rental_data_update_validation(self) -> None:
        pass

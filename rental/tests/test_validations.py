from rest_framework.test import APITestCase
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from address.models import Address
from client.models import Client
from staff.models import StaffMember
from branch.models import Branch
from vehicle.models import Vehicle, VehicleClassification
from ..models import Rental, Insurance, AdditionalItems
from .. import validators
from random import choice, choices, randrange
from validate_docbr import CPF, CNH, RENAVAM
import faker
import json


class ValidationsTestCase(APITestCase):
    def setUp(self) -> None:
        self.allow_field_update = validators.ALLOW_FIELD_UPDATE

        fake = faker.Faker('pt_BR')
        cpf = CPF()
        cnh = CNH()
        renavam = RENAVAM()

        def json_generator():
            data = dict()
            for _ in range(randrange(3, 8)):
                data[fake.words(nb=1)[0]] = ' '.join(fake.words(nb=2))
            return json.dumps(data)

        username = [fake.first_name() + str(randrange(10000, 99999)) for _ in range(4)]
        users = [User.objects.create_user(
            username=username[i],
            email=username[i] + '@email.com.br',
            password=username[i]
        ) for i in range(4)]

        addresses = [Address.objects.create(
            cep_address=fake.postcode(),
            state_address=fake.estado_sigla(),
            city_address=fake.city(),
            district_address=fake.bairro(),
            street_address=fake.street_name(),
            number_address=fake.building_number()
        ) for _ in range(5)]

        self.clients = [Client.objects.create(
            user_client=users[i],
            cpf_person=cpf.generate(),
            rg_person=fake.rg(),
            cnh_client=cnh.generate(),
            gender_person=choice(('M', 'F', 'N')),
            age_person=randrange(18, 99),
            finance_client=randrange(500, 30000),
            phone_person=fake.cellphone_number()[4:],
            address_person=addresses[i]
        ) for i in range(2)]

        self.branches = [Branch.objects.create(
            name_branch=fake.street_name(),
            opening_hours_start_branch=str(randrange(5, 13)) + ':00:00',
            opening_hours_end_branch=str(randrange(5, 13) + 8) + ':00:00',
            address_branch=addresses[2]
        ) for _ in range(2)]

        self.staffmembers = [StaffMember.objects.create(
            user_staffmember=users[i + 2],
            cpf_person=cpf.generate(),
            rg_person=fake.rg(),
            gender_person=choice(('M', 'F', 'N')),
            age_person=randrange(18, 99),
            salary_staffmember=randrange(500, 30000),
            phone_person=fake.cellphone_number()[4:],
            address_person=addresses[i + 3],
            branch_staffmember=self.branches[i]
        ) for i in range(2)]

        classifications = [VehicleClassification.objects.create(
            title_classification=' '.join(fake.words(nb=3)),
            daily_cost_classification=randrange(500, 5000) / 100
        ) for _ in range(2)]

        year_manufacture = randrange(1960, 2020)
        self.vehicles = [Vehicle.objects.create(
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
            branch_vehicle=self.branches[0],
            classification_vehicle=classifications[0]
        ) for _ in range(2)]

        self.insurances = [Insurance.objects.create(
            title_insurance=' '.join(fake.words(nb=2)),
            coverage_insurance=json_generator(),
            price_insurance=randrange(100, 2000) / 100
        ) for _ in range(2)]

        self.additional_items = [AdditionalItems.objects.create(
            name_additionalitems=' '.join(fake.words(nb=2)),
            daily_cost_additionalitems=randrange(50, 500) / 100
        ) for _ in range(2)]

        self.rental = Rental.objects.create(
            vehicle_rental=self.vehicles[0],
            staff_rental=self.staffmembers[0],
            client_rental=self.clients[0],
            status_rental='A',
            outlet_branch_rental=self.branches[0],
            appointment_date_rental=str(timezone.now() + timezone.timedelta(days=10))[:10],
            requested_days_rental=3,
            rent_deposit_rental=150,
            daily_cost_rental=randrange(500, 5000) / 100,
            additional_daily_cost_rental=0.
        )
        self.rental.driver_rental.set([self.clients[0], ])

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
            [False, False, True, False],
            [False, False, False, True],
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
        new_values = {
            'vehicle_rental': self.vehicles[1],
            'insurance_rental': self.insurances[1],
            'staff_rental': self.staffmembers[1],
            'client_rental': self.clients[1],
            'status_rental': 'A',
            'outlet_branch_rental': self.branches[1],
            'arrival_branch_rental': self.branches[0],
            'distance_branch_rental': randrange(5000, 10000),
            'appointment_date_rental': timezone.now() + timezone.timedelta(days=randrange(1, 2)),
            'rent_date_rental': timezone.now() + timezone.timedelta(days=randrange(1, 2)),
            'devolution_date_rental': timezone.now() + timezone.timedelta(days=randrange(6, 12)),
            'requested_days_rental': randrange(6, 10),
            'actual_days_rental': randrange(6, 10),
            'rent_deposit_rental': randrange(600, 1000),
            'daily_cost_rental': randrange(6000, 10000) / 100,
            'additional_daily_cost_rental': randrange(600, 1000) / 100,
            'additional_items_rental': self.additional_items,
            'driver_rental': self.clients
        }
        keys = ['vehicle_rental', 'insurance_rental', 'staff_rental', 'client_rental', 'status_rental',
                'outlet_branch_rental', 'arrival_branch_rental', 'distance_branch_rental', 'appointment_date_rental',
                'rent_date_rental', 'devolution_date_rental', 'requested_days_rental', 'actual_days_rental',
                'rent_deposit_rental', 'daily_cost_rental', 'additional_daily_cost_rental', 'additional_items_rental',
                'driver_rental', ]

        for current_status, new_status in zip(('A', 'L', 'C', 'D'), ('L', 'C', 'D', 'A')):
            new_values['status_rental'] = new_status
            self.rental.status_rental = current_status
            for key, value in new_values.items():
                validated_data = self.rental.__dict__
                validated_data = {key: validated_data[key] for key in keys if validated_data.get(key)}
                validated_data[key] = value
                response = key in self.allow_field_update[validated_data['status_rental']]
                self.assertEqual(validators.valid_rental_data_update(self.rental, validated_data)[0], response)

    def test_appointament_creation_date(self) -> None:
        entry_dates = [
            '',
            None,
            str(timezone.now() - timedelta(days=3))[:10],
            str(timezone.now())[:10],
            str(timezone.now() + timedelta(days=3))[:10],
        ]
        expected_response = [False, False, False, False, True]

        for i, entry in enumerate(entry_dates):
            self.assertEqual(validators.valid_appointment_creation(entry), expected_response[i])

    def test_the_validation_of_renting_a_vehicle(self) -> None:
        self.assertTrue(validators.valid_rented_vehicle(self.vehicles[0].renavam_vehicle, 5))

    def test_the_validation_of_renting_a_vehicle_with_a_vehicle_already_rented(self) -> None:
        self.assertTrue(validators.valid_rented_vehicle(self.vehicles[0].renavam_vehicle, 5))
        Rental.objects.create(
            vehicle_rental=self.vehicles[0],
            staff_rental=self.staffmembers[0],
            client_rental=self.clients[0],
            status_rental='L',
            outlet_branch_rental=self.branches[0],
            requested_days_rental=3,
            rent_deposit_rental=150,
            daily_cost_rental=randrange(500, 5000) / 100,
            additional_daily_cost_rental=0.
        )
        self.assertFalse(validators.valid_rented_vehicle(self.vehicles[0].renavam_vehicle, 5))

    def test_the_validation_of_renting_a_vehicle_with_a_vehicle_already_scheduled(self) -> None:
        self.assertTrue(validators.valid_rented_vehicle(self.vehicles[0].renavam_vehicle, 5))
        self.assertFalse(validators.valid_rented_vehicle(self.vehicles[0].renavam_vehicle, 7))
        self.assertFalse(validators.valid_rented_vehicle(self.vehicles[0].renavam_vehicle, 10))

    def test_the_validation_of_scheduling_a_vehicle(self) -> None:
        appointment_date = str(timezone.now() + timezone.timedelta(days=3))[:10]
        self.assertTrue(validators.valid_scheduled_vehicle(self.vehicles[0].renavam_vehicle, appointment_date, 3))

    def test_the_validation_of_scheduling_a_vehicle_with_a_vehicle_already_scheduled(self) -> None:
        entry_data = [
            (str(timezone.now() + timezone.timedelta(days=4))[:10], 3),
            (str(timezone.now() + timezone.timedelta(days=9))[:10], 3),
            (str(timezone.now() + timezone.timedelta(days=12))[:10], 7),
            (str(timezone.now() + timezone.timedelta(days=16))[:10], 3),
            (str(timezone.now() + timezone.timedelta(days=11))[:10], 1),
            (str(timezone.now() + timezone.timedelta(days=3))[:10], 30),
        ]
        for entry in entry_data:
            self.assertFalse(validators.valid_scheduled_vehicle(self.vehicles[0].renavam_vehicle, entry[0], entry[1]))

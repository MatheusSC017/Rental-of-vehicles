from random import choice, choices, randrange
from datetime import timedelta
import json
import faker
from rest_framework.test import APITestCase
from django.utils import timezone
from django.contrib.auth.models import User
from address.models import Address
from client.models import Client
from staff.models import StaffMember
from branch.models import Branch
from vehicle.models import Vehicle, VehicleClassification
from validate_docbr import CPF, CNH, RENAVAM
from unidecode import unidecode
from ..models import Rental, Insurance, AdditionalItems, RentalAdditionalItem
from .. import validators

fake = faker.Faker('pt_BR')
cpf_generator = CPF()
cnh_generator = CNH()
renavam_generator = RENAVAM()


class ValidationsTestCase(APITestCase):
    def setUp(self) -> None:
        self.allow_field_update = validators.ALLOW_FIELD_UPDATE

        def json_generator():
            data = {}
            for _ in range(randrange(3, 8)):
                data[fake.words(nb=1)[0]] = ' '.join(fake.words(nb=2))
            return json.dumps(data)

        username = [fake.first_name().replace(' ', '_') + str(randrange(10000, 99999)) for _ in range(4)]
        users = [User.objects.create_user(
            username=username[i],
            email=unidecode(username[i] + '@email.com.br'),
            password=username[i]
        ) for i in range(4)]

        addresses = [Address.objects.create(
            cep=fake.postcode(),
            state=fake.estado_sigla(),
            city=fake.city(),
            district=fake.bairro(),
            street=fake.street_name(),
            number=fake.building_number()
        ) for _ in range(5)]

        self.clients = [Client.objects.create(
            user=users[i],
            cpf=cpf_generator.generate(),
            rg=fake.rg(),
            cnh=cnh_generator.generate(),
            gender=choice(('M', 'F', 'N')),
            age=randrange(18, 99),
            finance=randrange(500, 30000),
            phone=fake.cellphone_number()[4:],
            address=addresses[i]
        ) for i in range(2)]

        self.branches = [Branch.objects.create(
            name=fake.street_name(),
            opening_hours_start=str(randrange(5, 13)) + ':00:00',
            opening_hours_end=str(randrange(5, 13) + 8) + ':00:00',
            address=addresses[2]
        ) for _ in range(2)]

        self.staffmembers = [StaffMember.objects.create(
            user=users[i + 2],
            cpf=cpf_generator.generate(),
            rg=fake.rg(),
            gender=choice(('M', 'F', 'N')),
            age=randrange(18, 99),
            salary=randrange(500, 30000),
            phone=fake.cellphone_number()[4:],
            address=addresses[i + 3],
            branch=self.branches[i]
        ) for i in range(2)]

        classifications = [VehicleClassification.objects.create(
            title=' '.join(fake.words(nb=3)),
            daily_cost=randrange(500, 5000) / 100
        ) for _ in range(2)]

        year_manufacture = randrange(1960, 2020)
        self.vehicles = [Vehicle.objects.create(
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
            branch=self.branches[0],
            classification=classifications[0]
        ) for _ in range(2)]

        self.insurances = [Insurance.objects.create(
            title=' '.join(fake.words(nb=2)),
            coverage=json_generator(),
            price=randrange(100, 2000) / 100
        ) for _ in range(2)]

        self.additional_items = [AdditionalItems.objects.create(
            name=' '.join(fake.words(nb=2)),
            daily_cost=randrange(50, 500) / 100,
            stock=randrange(5, 10),
            branch=self.branches[0]
        ) for _ in range(2)]

        self.rental = Rental.objects.create(
            vehicle=self.vehicles[0],
            staff=self.staffmembers[0],
            client=self.clients[0],
            status='A',
            outlet_branch=self.branches[0],
            appointment_date=str(timezone.now() + timezone.timedelta(days=10))[:10],
            requested_days=3,
            rent_deposit=150,
            daily_cost=randrange(500, 5000) / 100,
            additional_daily_cost=0.
        )
        self.rental.driver.set([self.clients[0], ])

    def test_initial_state_value_of(self) -> None:
        initial_values = ['A', 'L', 'C', 'D']
        output_values = []
        for inital_value in initial_values:
            output_values.append(validators.valid_rental_states_on_create(inital_value))
        self.assertEqual(output_values, [True, True, False, False])

    def test_update_state_value_of(self) -> None:
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

    def test_rental_data_update_validation(self) -> None:
        new_values = {
            'vehicle': self.vehicles[1],
            'insurance': self.insurances[1],
            'staff': self.staffmembers[1],
            'client': self.clients[1],
            'status': 'A',
            'outlet_branch': self.branches[1],
            'arrival_branch': self.branches[0],
            'distance_branch': randrange(5000, 10000),
            'appointment_date': timezone.now() + timezone.timedelta(days=randrange(1, 2)),
            'rent_date': timezone.now() + timezone.timedelta(days=randrange(1, 2)),
            'devolution_date': timezone.now() + timezone.timedelta(days=randrange(6, 12)),
            'requested_days': randrange(6, 10),
            'actual_days': randrange(6, 10),
            'rent_deposit': randrange(600, 1000),
            'daily_cost': randrange(6000, 10000) / 100,
            'additional_daily_cost': randrange(600, 1000) / 100,
            'driver': self.clients
        }
        keys = ['vehicle', 'insurance', 'staff', 'client', 'status', 'outlet_branch', 'arrival_branch',
                'distance_branch', 'appointment_date', 'rent_date', 'devolution_date', 'requested_days', 'actual_days',
                'rent_deposit', 'daily_cost', 'additional_daily_cost', 'additional_items', 'driver', ]

        for current_status, new_status in zip(('A', 'L', 'C', 'D'), ('L', 'C', 'D', 'A')):
            new_values['status'] = new_status
            self.rental.status = current_status
            for key, value in new_values.items():
                validated_data = self.rental.__dict__
                validated_data = {key: validated_data[key] for key in keys if validated_data.get(key)}
                validated_data[key] = value
                response = key in self.allow_field_update[validated_data['status']]
                self.assertEqual(validators.valid_rental_data_update(self.rental, validated_data)[0], response)

    def test_appointament_creation_date(self) -> None:
        entry_dates = [
            '',
            None,
            str(timezone.now() - timedelta(days=3))[:10],
            str(timezone.now())[:10],
            str(timezone.now() + timedelta(days=3))[:10],
            str(timezone.now() + timedelta(days=15))[:10],
            str(timezone.now() + timedelta(days=100))[:10],
            str(timezone.now() + timedelta(days=400))[:10],
        ]
        expected_response = [False, False, False, False, True, True, True, False]

        for i, entry in enumerate(entry_dates):
            self.assertEqual(validators.valid_appointment_creation(entry), expected_response[i])

    def test_the_validation_of_renting_a_vehicle(self) -> None:
        self.assertTrue(validators.valid_rented_vehicle(self.vehicles[0].renavam, 5))

    def test_the_validation_of_renting_a_vehicle_with_a_vehicle_already_rented(self) -> None:
        self.assertTrue(validators.valid_rented_vehicle(self.vehicles[0].renavam, 5))
        Rental.objects.create(
            vehicle=self.vehicles[0],
            staff=self.staffmembers[0],
            client=self.clients[0],
            status='L',
            outlet_branch=self.branches[0],
            requested_days=3,
            rent_deposit=150,
            daily_cost=randrange(500, 5000) / 100,
            additional_daily_cost=0.
        )
        self.assertFalse(validators.valid_rented_vehicle(self.vehicles[0].renavam, 5))

    def test_the_validation_of_renting_a_vehicle_with_a_vehicle_already_scheduled(self) -> None:
        self.assertTrue(validators.valid_rented_vehicle(self.vehicles[0].renavam, 5))
        self.assertFalse(validators.valid_rented_vehicle(self.vehicles[0].renavam, 7))
        self.assertFalse(validators.valid_rented_vehicle(self.vehicles[0].renavam, 10))

    def test_the_validation_of_scheduling_a_vehicle(self) -> None:
        appointment_date = str(timezone.now() + timezone.timedelta(days=3))[:10]
        self.assertTrue(validators.valid_scheduled_vehicle(self.vehicles[0].renavam, appointment_date, 3))

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
            self.assertFalse(validators.valid_scheduled_vehicle(self.vehicles[0].renavam, entry[0], entry[1]))

    def test_the_validation_of_renting_a_vehicle_to_change_requested_days(self) -> None:
        rental = Rental.objects.create(
            vehicle=self.vehicles[0],
            staff=self.staffmembers[0],
            client=self.clients[0],
            status='L',
            outlet_branch=self.branches[0],
            requested_days=3,
            rent_deposit=150,
            daily_cost=randrange(500, 5000) / 100,
            additional_daily_cost=0.
        )
        self.assertTrue(validators.valid_rented_vehicle(self.vehicles[0].renavam, 5, rental.pk))

    def test_the_validation_of_renting_a_vehicle_to_change_requested_days_with_a_vehicle_already_schedule(self) -> None:
        rental = Rental.objects.create(
            vehicle=self.vehicles[0],
            staff=self.staffmembers[0],
            client=self.clients[0],
            status='L',
            outlet_branch=self.branches[0],
            requested_days=3,
            rent_deposit=150,
            daily_cost=randrange(500, 5000) / 100,
            additional_daily_cost=0.
        )
        self.assertFalse(validators.valid_rented_vehicle(self.vehicles[0].renavam, 10, rental.pk))

    def test_the_validation_of_scheduling_a_vehicle_to_change_requested_days(self) -> None:
        rental = Rental.objects.create(
            vehicle=self.vehicles[0],
            staff=self.staffmembers[0],
            client=self.clients[0],
            status='A',
            appointment_date=str(timezone.now() + timezone.timedelta(days=3))[:10],
            outlet_branch=self.branches[0],
            requested_days=3,
            rent_deposit=150,
            daily_cost=randrange(500, 5000) / 100,
            additional_daily_cost=0.
        )
        appointment_date = str(timezone.now() + timezone.timedelta(days=17))[:10]
        self.assertTrue(validators.valid_scheduled_vehicle(renavam=self.vehicles[0].renavam,
                                                           requested_days=3,
                                                           appointment_date=appointment_date,
                                                           id_rental=rental.pk))

    def test_the_validation_of_scheduling_to_change_requested_days_with_a_vehicle_already_scheduled(self) -> None:
        rental = Rental.objects.create(
            vehicle=self.vehicles[0],
            staff=self.staffmembers[0],
            client=self.clients[0],
            status='A',
            appointment_date=str(timezone.now() + timezone.timedelta(days=3))[:10],
            outlet_branch=self.branches[0],
            requested_days=3,
            rent_deposit=150,
            daily_cost=randrange(500, 5000) / 100,
            additional_daily_cost=0.
        )

        entry_values = [
            (str(timezone.now() + timezone.timedelta(days=5))[:10], 6),
            (str(timezone.now() + timezone.timedelta(days=11))[:10], 10),
            (str(timezone.now() + timezone.timedelta(days=5))[:10], 15),
            (str(timezone.now() + timezone.timedelta(days=11))[:10], 1),
        ]

        for appointment_date, requested_days in entry_values:
            self.assertFalse(validators.valid_scheduled_vehicle(renavam=self.vehicles[0].renavam,
                                                                requested_days=requested_days,
                                                                appointment_date=appointment_date,
                                                                id_rental=rental.pk))

    def test_function_additional_items_updated_no_additional_items(self):
        self.assertFalse(validators.additional_items_updated(self.rental.pk, []))
        self.assertTrue(validators.additional_items_updated(self.rental.pk,
                                                            [{'additional_item': self.additional_items[0],
                                                              'number': randrange(1, 3)}, ]))

    def test_function_additional_items_updated(self):
        additional_items_data = [{'additional_item': item, 'number': randrange(1, 3)}
                                 for item in self.additional_items]
        for additional_item in additional_items_data:
            RentalAdditionalItem.objects.create(rental=self.rental, **additional_item)
        self.assertFalse(validators.additional_items_updated(self.rental.pk, additional_items_data))
        additional_items_data[1]['number'] = randrange(4, 5)
        self.assertTrue(validators.additional_items_updated(self.rental.pk, additional_items_data))
        additional_items_data.pop()
        self.assertTrue(validators.additional_items_updated(self.rental.pk, additional_items_data))

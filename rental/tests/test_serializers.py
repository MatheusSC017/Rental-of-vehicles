from django.test import TestCase
from django.utils import timezone
from utils.mixins.serializers import GetRelationOfTheFieldMixin
from ..serializers import InsuranceSerializer, AdditionalItemsSerializer, RentalSerializer
from ..models import Insurance, AdditionalItems, Rental
from django.contrib.auth.models import User, Permission, ContentType
from address.models import Address
from client.models import Client
from staff.models import StaffMember
from branch.models import Branch
from vehicle.models import Vehicle, VehicleClassification
from random import choice, choices, randrange
from validate_docbr import CPF, CNH, RENAVAM
from unidecode import unidecode
import faker
import json


class InsuranceSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.insurance = Insurance.objects.create(
            title_insurance='InsuranceTitle',
            coverage_insurance=json.dumps({'Coverage': 100000., 'Steal': 30000.}),
            price_insurance=5.
        )
        self.serializer = InsuranceSerializer(instance=self.insurance)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'title_insurance', 'coverage_insurance', 'price_insurance'})

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(data['title_insurance'], self.insurance.title_insurance)
        self.assertEqual(data['coverage_insurance'], self.insurance.coverage_insurance)
        self.assertEqual(data['price_insurance'], self.insurance.price_insurance)


class AdditionalItemsSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.additional_item = AdditionalItems.objects.create(
            name_additionalitems='Additional Item Name',
            daily_cost_additionalitems=2.5
        )

        self.serializer = AdditionalItemsSerializer(self.additional_item)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name_additionalitems', 'daily_cost_additionalitems'})

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(data['name_additionalitems'], self.additional_item.name_additionalitems)
        self.assertEqual(data['daily_cost_additionalitems'], self.additional_item.daily_cost_additionalitems)


class RentalSerializerTestCase(TestCase, GetRelationOfTheFieldMixin):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')
        cpf = CPF()
        cnh = CNH()
        renavam = RENAVAM()

        def json_generator():
            data = dict()
            for _ in range(randrange(3, 8)):
                data[fake.words(nb=1)[0]] = ' '.join(fake.words(nb=2))
            return json.dumps(data)

        usernames = [fake.first_name().replace(' ', '_') + str(randrange(10000, 99999)) for _ in range(3)]
        self.user_staff, user_client_1, user_client_2 = [User.objects.create_user(
            username=username,
            email=unidecode(username + '@email.com.br'),
            password=username
        ) for username in usernames]

        content_type = ContentType.objects.get_for_model(Rental)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user_staff.user_permissions.add(permission)

        addresses = [Address.objects.create(
            cep_address=fake.postcode(),
            state_address=fake.estado_sigla(),
            city_address=fake.city(),
            district_address=fake.bairro(),
            street_address=fake.street_name(),
            number_address=fake.building_number()
        ) for _ in range(4)]

        self.clients = [Client.objects.create(
            user_client=user_client,
            cpf_person=cpf.generate(),
            rg_person=fake.rg(),
            cnh_client=cnh.generate(),
            gender_person=choice(('M', 'F', 'N')),
            age_person=randrange(18, 99),
            finance_client=randrange(500, 30000),
            phone_person=fake.cellphone_number()[4:],
            address_person=addresses[0]
        ) for user_client in (user_client_1, user_client_2)]

        branch = Branch.objects.create(
            name_branch=fake.street_name(),
            opening_hours_start_branch=str(randrange(5, 13)) + ':00:00',
            opening_hours_end_branch=str(randrange(5, 13) + 8) + ':00:00',
            address_branch=addresses[1]
        )

        staffmember = StaffMember.objects.create(
            user_staffmember=self.user_staff,
            cpf_person=cpf.generate(),
            rg_person=fake.rg(),
            gender_person=choice(('M', 'F', 'N')),
            age_person=randrange(18, 99),
            salary_staffmember=randrange(500, 30000),
            phone_person=fake.cellphone_number()[4:],
            address_person=addresses[2],
            branch_staffmember=branch
        )

        daily_cost = randrange(500, 5000) / 100
        classification = VehicleClassification.objects.create(
            title_classification=' '.join(fake.words(nb=3)),
            daily_cost_classification=daily_cost
        )

        year_manufacture = randrange(1960, 2020)
        self.vehicle = Vehicle.objects.create(
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
            branch_vehicle=branch,
            classification_vehicle=classification
        )

        insurance = Insurance.objects.create(
            title_insurance=' '.join(fake.words(nb=2)),
            coverage_insurance=json_generator(),
            price_insurance=randrange(100, 2000) / 100
        )

        self.rental = Rental.objects.create(
            vehicle_rental=self.vehicle,
            staff_rental=staffmember,
            client_rental=self.clients[0],
            status_rental='A',
            outlet_branch_rental=branch,
            appointment_date_rental=str(timezone.now())[:10],
            requested_days_rental=3,
            rent_deposit_rental=150,
            daily_cost_rental=daily_cost,
            additional_daily_cost_rental=0.,
            insurance_rental=insurance
        )
        self.rental.driver_rental.set(self.clients)

        self.keys = {'id', 'vehicle_rental', 'insurance_rental', 'staff_rental', 'client_rental', 'status_rental',
                     'outlet_branch_rental', 'arrival_branch_rental', 'distance_branch_rental', 'driver_rental',
                     'appointment_date_rental', 'rent_date_rental', 'devolution_date_rental', 'requested_days_rental',
                     'actual_days_rental', 'rent_deposit_rental', 'daily_cost_rental', 'total_cost_rental',
                     'additional_daily_cost_rental', 'additional_items_rental', 'return_rate_rental', 'fines_rental',
                     'devolution_date_expected_rental'}
        self.serializer = RentalSerializer(self.rental)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), self.keys)

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        many_to_many, objects = self.get_many_to_many_and_objects_fields(Rental)
        for key in self.keys:
            if key in many_to_many:
                self.assertEqual(set(data.get(key)),
                                 set([field.__repr__() for field in getattr(self.rental, key).all()]),
                                 msg=f"The content of {key} is wrong")
            elif key in objects:
                self.assertEqual(str(data.get(key)), str(getattr(self.rental, key).__repr__()),
                                 msg=f"The content of {key} is wrong")
            else:
                self.assertEqual(data.get(key), getattr(self.rental, key),
                                 msg=f"The content of {key} is wrong")

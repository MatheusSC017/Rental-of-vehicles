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
            title='InsuranceTitle',
            coverage=json.dumps({'Coverage': 100000., 'Steal': 30000.}),
            price=5.
        )
        self.serializer = InsuranceSerializer(instance=self.insurance)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'title', 'coverage', 'price'})

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(data['title'], self.insurance.title)
        self.assertEqual(data['coverage'], self.insurance.coverage)
        self.assertEqual(data['price'], self.insurance.price)


class AdditionalItemsSerializerTestCase(TestCase):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')

        address = Address.objects.create(
            cep=fake.postcode(),
            state=fake.estado_sigla(),
            city=fake.city(),
            district=fake.bairro(),
            street=fake.street_name(),
            number=fake.building_number()
        )

        branch = Branch.objects.create(
            name=fake.street_name(),
            opening_hours_start=str(randrange(5, 13)) + ':00:00',
            opening_hours_end=str(randrange(5, 13) + 8) + ':00:00',
            address=address
        )

        self.additional_item = AdditionalItems.objects.create(
            name='Additional Item Name',
            daily_cost=2.5,
            stock=3,
            branch=branch
        )

        self.serializer = AdditionalItemsSerializer(self.additional_item)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'name', 'daily_cost',
                                            'stock', 'branch'})

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(data['name'], self.additional_item.name)
        self.assertEqual(data['daily_cost'], self.additional_item.daily_cost)


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
            cep=fake.postcode(),
            state=fake.estado_sigla(),
            city=fake.city(),
            district=fake.bairro(),
            street=fake.street_name(),
            number=fake.building_number()
        ) for _ in range(4)]

        self.clients = [Client.objects.create(
            user=user_client,
            cpf=cpf.generate(),
            rg=fake.rg(),
            cnh=cnh.generate(),
            gender=choice(('M', 'F', 'N')),
            age=randrange(18, 99),
            finance=randrange(500, 30000),
            phone=fake.cellphone_number()[4:],
            address=addresses[0]
        ) for user_client in (user_client_1, user_client_2)]

        branch = Branch.objects.create(
            name=fake.street_name(),
            opening_hours_start=str(randrange(5, 13)) + ':00:00',
            opening_hours_end=str(randrange(5, 13) + 8) + ':00:00',
            address=addresses[1]
        )

        staffmember = StaffMember.objects.create(
            user=self.user_staff,
            cpf=cpf.generate(),
            rg=fake.rg(),
            gender=choice(('M', 'F', 'N')),
            age=randrange(18, 99),
            salary=randrange(500, 30000),
            phone=fake.cellphone_number()[4:],
            address=addresses[2],
            branch=branch
        )

        daily_cost = randrange(500, 5000) / 100
        classification = VehicleClassification.objects.create(
            title=' '.join(fake.words(nb=3)),
            daily_cost=daily_cost
        )

        year_manufacture = randrange(1960, 2020)
        self.vehicle = Vehicle.objects.create(
            type=choice('MC'),
            brand=' '.join(fake.words(nb=1)),
            model=' '.join(fake.words(nb=2)),
            year_manufacture=year_manufacture,
            model_year=year_manufacture + randrange(0, 5),
            mileage=float(randrange(0, 2000)),
            renavam=renavam.generate(),
            license_plate=fake.license_plate().replace('-', ''),
            chassi=str(randrange(11111111111111111, 99999999999999999)),
            fuel=choice('GEDH'),
            fuel_tank=randrange(15, 50),
            engine=' '.join(fake.words()),
            color=fake.color_name(),
            other_data=json_generator(),
            available=choices([True, False], weights=(90, 10))[0],
            branch=branch,
            classification=classification
        )

        insurance = Insurance.objects.create(
            title=' '.join(fake.words(nb=2)),
            coverage=json_generator(),
            price=randrange(100, 2000) / 100
        )

        self.rental = Rental.objects.create(
            vehicle=self.vehicle,
            staff=staffmember,
            client=self.clients[0],
            status='A',
            outlet_branch=branch,
            appointment_date=str(timezone.now())[:10],
            requested_days=3,
            rent_deposit=150,
            daily_cost=daily_cost,
            additional_daily_cost=0.,
            insurance=insurance
        )
        self.rental.driver.set(self.clients)

        self.keys = {'id', 'vehicle', 'insurance', 'staff', 'client', 'status',
                     'outlet_branch', 'arrival_branch', 'distance_branch', 'driver',
                     'appointment_date', 'rent_date', 'devolution_date', 'requested_days',
                     'actual_days', 'rent_deposit', 'daily_cost', 'total_cost',
                     'additional_daily_cost', 'additional_items', 'return_rate', 'fines', }
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

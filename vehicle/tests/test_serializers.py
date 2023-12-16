from random import randrange
import faker
from django.test import TestCase
from utils.mixins.serializers import GetRelationOfTheFieldMixin
from address.models import Address
from branch.models import Branch
from validate_docbr import RENAVAM
from ..models import VehicleClassification, Vehicle
from ..serializers import VehicleClassificationSerializer, VehicleSerializer


class VehicleClassificationSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.classification = VehicleClassification.objects.create(
            title='Vehicle Classification',
            daily_cost=7.5
        )
        self.serializer = VehicleClassificationSerializer(self.classification)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'title', 'daily_cost', })

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(data['title'], self.classification.title)
        self.assertEqual(data['daily_cost'], self.classification.daily_cost)


class VehicleSerializerTestCase(TestCase, GetRelationOfTheFieldMixin):
    def setUp(self) -> None:
        renavam = RENAVAM()
        fake = faker.Faker('pt_BR')

        address = Address.objects.create(
            cep=fake.postcode(),
            state=fake.estado_sigla(),
            city=fake.city(),
            district=fake.bairro(),
            street=fake.street_name(),
            number=fake.building_number()
        )

        start = randrange(5, 13)
        branch = Branch.objects.create(
            name=fake.street_name(),
            opening_hours_start=str(start) + ':00:00',
            opening_hours_end=str(start + 8) + ':00:00',
            address=address
        )

        classification = VehicleClassification.objects.create(
            title='Vehicle Classification',
            daily_cost=7.5
        )

        self.vehicle = Vehicle.objects.create(
            type='C',
            brand='FIAT',
            model='UNO',
            year_manufacture=2012,
            model_year=2014,
            mileage=10000,
            renavam=renavam.generate(),
            license_plate=fake.license_plate().replace('-', ''),
            chassi=str(randrange(11111111111111111, 99999999999999999)),
            fuel='E',
            fuel_tank=40,
            engine='40 CV',
            color='Vermelho',
            branch=branch,
            classification=classification
        )

        self.keys = {'type', 'brand', 'model', 'year_manufacture', 'model_year', 'mileage', 'renavam', 'license_plate',
                     'chassi', 'fuel', 'fuel_tank', 'engine', 'color', 'other_data', 'available', 'branch',
                     'classification', }

        self.serializer = VehicleSerializer(self.vehicle)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), self.keys)

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data

        _, objects = self.get_many_to_many_and_objects_fields(Vehicle)

        for key in self.keys:
            if key in objects:
                self.assertEqual(str(data[key]), repr(getattr(self.vehicle, key)))
            else:
                self.assertEqual(data[key], getattr(self.vehicle, key))

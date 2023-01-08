from django.test import TestCase
from utils.mixins.serializers import GetRelationOfTheFieldMixin
from address.models import Address
from branch.models import Branch
from ..models import VehicleClassification, Vehicle
from ..serializers import VehicleClassificationSerializer, VehicleSerializer
from validate_docbr import RENAVAM
from random import randrange
import faker


class VehicleClassificationSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.classification = VehicleClassification.objects.create(
            title_classification='Vehicle Classification',
            daily_cost_classification=7.5
        )
        self.serializer = VehicleClassificationSerializer(self.classification)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'title_classification', 'daily_cost_classification', })

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(data['title_classification'], self.classification.title_classification)
        self.assertEqual(data['daily_cost_classification'], self.classification.daily_cost_classification)


class VehicleSerializerTestCase(TestCase, GetRelationOfTheFieldMixin):
    def setUp(self) -> None:
        renavam = RENAVAM()
        fake = faker.Faker('pt_BR')

        address = Address.objects.create(
            cep_address=fake.postcode(),
            state_address=fake.estado_sigla(),
            city_address=fake.city(),
            district_address=fake.bairro(),
            street_address=fake.street_name(),
            number_address=fake.building_number()
        )

        start = randrange(5, 13)
        branch = Branch.objects.create(
            name_branch=fake.street_name(),
            opening_hours_start_branch=str(start) + ':00:00',
            opening_hours_end_branch=str(start + 8) + ':00:00',
            address_branch=address
        )

        classification = VehicleClassification.objects.create(
            title_classification='Vehicle Classification',
            daily_cost_classification=7.5
        )

        self.vehicle = Vehicle.objects.create(
            type_vehicle='C',
            brand_vehicle='FIAT',
            model_vehicle='UNO',
            year_manufacture_vehicle=2012,
            model_year_vehicle=2014,
            mileage_vehicle=10000,
            renavam_vehicle=renavam.generate(),
            license_plate_vehicle=fake.license_plate().replace('-', ''),
            chassi_vehicle=str(randrange(11111111111111111, 99999999999999999)),
            fuel_vehicle='E',
            fuel_tank_vehicle=40,
            engine_vehicle='40 CV',
            color_vehicle='Vermelho',
            branch_vehicle=branch,
            classification_vehicle=classification
        )

        self.keys = {'type_vehicle', 'brand_vehicle', 'model_vehicle', 'year_manufacture_vehicle', 'model_year_vehicle',
                     'mileage_vehicle', 'renavam_vehicle', 'license_plate_vehicle', 'chassi_vehicle', 'fuel_vehicle',
                     'fuel_tank_vehicle', 'engine_vehicle', 'color_vehicle', 'other_data_vehicle', 'available_vehicle',
                     'branch_vehicle', 'classification_vehicle', }

        self.serializer = VehicleSerializer(self.vehicle)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), self.keys)

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data

        _, objects = self.get_many_to_many_and_objects_fields(Vehicle)

        for key in self.keys:
            if key in objects:
                self.assertEqual(data[key], getattr(self.vehicle, key).__repr__())
            else:
                self.assertEqual(data[key], getattr(self.vehicle, key))

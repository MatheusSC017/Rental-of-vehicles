from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User, Permission, ContentType
from ..models import Vehicle, VehicleClassification
from branch.models import Branch
from address.models import Address
from random import randrange
from validate_docbr import RENAVAM
import faker


class VehicleClassificationViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.fake = faker.Faker('pt_BR')

        username = self.fake.first_name() + str(randrange(10000, 99999))
        self.user = User.objects.create_user(
            username=username,
            email=username + '@email.com',
            password=username
        )

        content_type = ContentType.objects.get_for_model(VehicleClassification)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user.user_permissions.add(permission)

        self.vehicle_classification = VehicleClassification.objects.create(
            title_classification=' '.join(self.fake.words(nb=2)),
            daily_cost_classification=randrange(5, 50)
        )

        self.list_url = reverse('Classifications-list')
        self.detail_url = reverse('Classifications-detail', kwargs={'pk': self.vehicle_classification.pk})

    def test_request_to_classification_list(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_classification_creation(self) -> None:
        self.client.force_login(self.user)
        data = {
            'title_classification': ' '.join(self.fake.words(nb=2)),
            'daily_cost_classification': randrange(5, 50)
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_to_classification_detail(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_classification_update(self) -> None:
        self.client.force_login(self.user)
        data = {
            'title_classification': ' '.join(self.fake.words(nb=2)),
            'daily_cost_classification': randrange(5, 50)
        }
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_classification_delete(self) -> None:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class VehicleViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.fake = faker.Faker('pt_BR')
        self.renavam = RENAVAM()

        username = self.fake.first_name() + str(randrange(10000, 99999))
        self.user = User.objects.create_user(
            username=username,
            email=username + '@email.com',
            password=username
        )

        content_type = ContentType.objects.get_for_model(Vehicle)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user.user_permissions.add(permission)

        address = Address.objects.create(
            cep_address=self.fake.postcode(),
            state_address=self.fake.estado_sigla(),
            city_address=self.fake.city(),
            district_address=self.fake.bairro(),
            street_address=self.fake.street_name(),
            number_address=self.fake.building_number()
        )

        self.branch = Branch.objects.create(
            name_branch=self.fake.street_name(),
            opening_hours_start_branch=str(randrange(5, 13)) + ':00:00',
            opening_hours_end_branch=str(randrange(5, 13) + 8) + ':00:00',
            address_branch=address
        )

        self.vehicle_classification = VehicleClassification.objects.create(
            title_classification='ClassificationTitle',
            daily_cost_classification=5.
        )

        vehicles = [Vehicle.objects.create(
            type_vehicle='C',
            brand_vehicle='FIAT',
            model_vehicle='UNO',
            year_manufacture_vehicle='2016',
            model_year_vehicle='2018',
            mileage_vehicle=1000,
            renavam_vehicle=self.renavam.generate(),
            license_plate_vehicle=self.fake.license_plate().replace('-', ''),
            chassi_vehicle=randrange(11111111111111111, 99999999999999999),
            fuel_vehicle='G',
            fuel_tank_vehicle=40,
            engine_vehicle='1.3, 59 CV',
            color_vehicle='Red',
            branch_vehicle=self.branch,
            available_vehicle=available,
            classification_vehicle=self.vehicle_classification
        ) for available in [True, False]]

        self.list_url = reverse('Vehicles-list')
        self.detail_url = reverse('Vehicles-detail', kwargs={'pk': vehicles[0].renavam_vehicle})

    def test_request_to_vehicle_available_list(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_request_to_vehicle_all_list(self) -> None:
        response = self.client.get(self.list_url, {'show_all': 1})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_request_to_vehicle_creation(self) -> None:
        self.client.force_login(self.user)
        data = {
            'type_vehicle': 'M',
            'brand_vehicle': 'Honda',
            'model_vehicle': 'Tita',
            'year_manufacture_vehicle': '2015',
            'model_year_vehicle': '2017',
            'mileage_vehicle': 2000.0,
            'renavam_vehicle': self.renavam.generate(),
            'license_plate_vehicle': self.fake.license_plate().replace('-', ''),
            'chassi_vehicle': '01234567890123456',
            'fuel_vehicle': 'E',
            'fuel_tank_vehicle': 20,
            'engine_vehicle': '1.0, 32 CV',
            'color_vehicle': 'Green',
            'branch_vehicle': self.branch.pk,
            'classification_vehicle': self.vehicle_classification.pk
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_to_vehicle_detail(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_vehicle_update(self) -> None:
        self.client.force_login(self.user)
        data = {
            'type_vehicle': 'M',
            'brand_vehicle': 'Honda',
            'model_vehicle': 'Tita',
            'year_manufacture_vehicle': '2015',
            'model_year_vehicle': '2017',
            'mileage_vehicle': 2000.0,
            'renavam_vehicle': self.renavam.generate(),
            'license_plate_vehicle': self.fake.license_plate().replace('-', ''),
            'chassi_vehicle': '01234567890123456',
            'fuel_vehicle': 'E',
            'fuel_tank_vehicle': 20,
            'engine_vehicle': '1.0, 32 CV',
            'color_vehicle': 'Green',
            'branch_vehicle': self.branch.pk,
            'classification_vehicle': self.vehicle_classification.pk
        }
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_vehicle_delete(self) -> None:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

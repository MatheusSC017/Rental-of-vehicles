from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User, Permission, ContentType
from ..models import Vehicle, VehicleClassification
from branch.models import Branch
from address.models import Address
from random import randrange
from validate_docbr import RENAVAM
from unidecode import unidecode
import faker


class VehicleClassificationViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.fake = faker.Faker('pt_BR')

        username = self.fake.first_name().replace(' ', '_') + str(randrange(10000, 99999))
        self.user = User.objects.create_user(
            username=username,
            email=unidecode(username + '@email.com'),
            password=username
        )

        content_type = ContentType.objects.get_for_model(VehicleClassification)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user.user_permissions.add(permission)

        self.vehicle_classification = VehicleClassification.objects.create(
            title=' '.join(self.fake.words(nb=2)),
            daily_cost=randrange(5, 50)
        )

        self.list_url = reverse('Classifications-list')
        self.detail_url = reverse('Classifications-detail', kwargs={'pk': self.vehicle_classification.pk})

    def test_request_to_classification_list(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_classification_creation(self) -> None:
        self.client.force_login(self.user)
        data = {
            'title': ' '.join(self.fake.words(nb=2)),
            'daily_cost': randrange(5, 50)
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_to_classification_detail(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_classification_update(self) -> None:
        self.client.force_login(self.user)
        data = {
            'title': ' '.join(self.fake.words(nb=2)),
            'daily_cost': randrange(5, 50)
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

        username = self.fake.first_name().replace(' ', '_') + str(randrange(10000, 99999))
        self.user = User.objects.create_user(
            username=username,
            email=unidecode(username + '@email.com'),
            password=username
        )

        content_type = ContentType.objects.get_for_model(Vehicle)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user.user_permissions.add(permission)

        address = Address.objects.create(
            cep=self.fake.postcode(),
            state=self.fake.estado_sigla(),
            city=self.fake.city(),
            district=self.fake.bairro(),
            street=self.fake.street_name(),
            number=self.fake.building_number()
        )

        self.branch = Branch.objects.create(
            name=self.fake.street_name(),
            opening_hours_start=str(randrange(5, 13)) + ':00:00',
            opening_hours_end=str(randrange(5, 13) + 8) + ':00:00',
            address=address
        )

        self.vehicle_classification = VehicleClassification.objects.create(
            title='ClassificationTitle',
            daily_cost=5.
        )

        vehicles = [Vehicle.objects.create(
            type='C',
            brand='FIAT',
            model='UNO',
            year_manufacture='2016',
            model_year='2018',
            mileage=1000,
            renavam=self.renavam.generate(),
            license_plate=self.fake.license_plate().replace('-', ''),
            chassi=randrange(11111111111111111, 99999999999999999),
            fuel='G',
            fuel_tank=40,
            engine='1.3, 59 CV',
            color='Red',
            branch=self.branch,
            available=available,
            classification=self.vehicle_classification
        ) for available in [True, False]]

        self.list_url = reverse('Vehicles-list')
        self.detail_url = reverse('Vehicles-detail', kwargs={'pk': vehicles[0].renavam})

    def test_request_to_vehicle_available_list(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_request_to_vehicle_all_list(self) -> None:
        response = self.client.get(self.list_url, {'show_all': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_request_to_vehicle_creation(self) -> None:
        self.client.force_login(self.user)
        data = {
            'type': 'M',
            'brand': 'Honda',
            'model': 'Tita',
            'year_manufacture': '2015',
            'model_year': '2017',
            'mileage': 2000.0,
            'renavam': self.renavam.generate(),
            'license_plate': self.fake.license_plate().replace('-', ''),
            'chassi': '01234567890123456',
            'fuel': 'E',
            'fuel_tank': 20,
            'engine': '1.0, 32 CV',
            'color': 'Green',
            'branch': self.branch.pk,
            'classification': self.vehicle_classification.pk
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_to_vehicle_detail(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_vehicle_update(self) -> None:
        self.client.force_login(self.user)
        data = {
            'type': 'M',
            'brand': 'Honda',
            'model': 'Tita',
            'year_manufacture': '2015',
            'model_year': '2017',
            'mileage': 2000.0,
            'renavam': self.renavam.generate(),
            'license_plate': self.fake.license_plate().replace('-', ''),
            'chassi': '01234567890123456',
            'fuel': 'E',
            'fuel_tank': 20,
            'engine': '1.0, 32 CV',
            'color': 'Green',
            'branch': self.branch.pk,
            'classification': self.vehicle_classification.pk
        }
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_vehicle_delete(self) -> None:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

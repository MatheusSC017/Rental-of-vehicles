import faker
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User, Permission, ContentType
from address.models import Address
from vehicle.models import Vehicle
from unidecode import unidecode
from ..models import Branch


class BranchViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')

        username = fake.first_name().replace(' ', '_') + '123456789'
        self.user = User.objects.create_user(
            username=username,
            email=unidecode(username + '@email.com'),
            password=username
        )

        content_type = ContentType.objects.get_for_model(Branch)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user.user_permissions.add(permission)

        self.address = Address.objects.create(
            cep=fake.postcode(),
            state=fake.estado_sigla(),
            city=fake.city(),
            district=fake.bairro(),
            street=fake.street_name(),
            number=fake.building_number()
        )

        self.branch = Branch.objects.create(
            name=fake.street_name(),
            opening_hours_start='07:00:00',
            opening_hours_end='17:00:00',
            address=self.address
        )

        self.list_url = reverse('Branches-list')
        self.detail_url = reverse('Branches-detail', kwargs={'pk': self.branch.pk})

    def test_request_to_branch_list(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_branch_creation(self) -> None:
        self.client.force_login(self.user)
        data = {
            'name': 'Branch name',
            'opening_hours_start': '07:00:00',
            'opening_hours_end': '17:00:00',
            'address': self.address.pk,
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_to_branch_detail(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_branch_update(self) -> None:
        self.client.force_login(self.user)
        data = {
            'name': 'Branch name',
            'opening_hours_start': '08:00:00',
            'opening_hours_end': '18:00:00',
            'address': self.address.pk,
        }
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_branch_delete(self) -> None:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class BranchAddressViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')

        username = fake.first_name().replace(' ', '_') + '123456789'
        self.user = User.objects.create_user(
            username=username,
            email=unidecode(username + '@email.com'),
            password=username
        )

        content_type = ContentType.objects.get_for_model(Address)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user.user_permissions.add(permission)

        self.address = Address.objects.create(
            cep=fake.postcode(),
            state=fake.estado_sigla(),
            city=fake.city(),
            district=fake.bairro(),
            street=fake.street_name(),
            number=fake.building_number()
        )

        self.branch = Branch.objects.create(
            name=fake.street_name(),
            opening_hours_start='07:00:00',
            opening_hours_end='17:00:00',
            address=self.address
        )

        self.list_url = reverse('BranchAddresses-list', kwargs={'pk': self.branch.pk})

    def test_request_to_branch_list(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_branch_creation(self) -> None:
        self.client.force_login(self.user)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class BranchVehicleViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')

        username = fake.first_name().replace(' ', '_') + '123456789'
        self.user = User.objects.create_user(
            username=username,
            email=unidecode(username + '@email.com'),
            password=username
        )

        content_type = ContentType.objects.get_for_model(Vehicle)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user.user_permissions.add(permission)

        self.address = Address.objects.create(
            cep=fake.postcode(),
            state=fake.estado_sigla(),
            city=fake.city(),
            district=fake.bairro(),
            street=fake.street_name(),
            number=fake.building_number()
        )

        self.branch = Branch.objects.create(
            name=fake.street_name(),
            opening_hours_start='07:00:00',
            opening_hours_end='17:00:00',
            address=self.address
        )

        self.list_url = reverse('BranchVehicles-list', kwargs={'pk': self.branch.pk})

    def test_request_to_branch_vehicle_list(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_branch_vehicle_creation(self) -> None:
        self.client.force_login(self.user)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

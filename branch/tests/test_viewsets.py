from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User, Permission, ContentType
from ..models import Branch
from address.models import Address
import faker


class BranchViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')

        username = fake.first_name() + '123456789'
        self.user = User.objects.create_user(
            username=username,
            email=username + '@email.com',
            password=username
        )

        content_type = ContentType.objects.get_for_model(Branch)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user.user_permissions.add(permission)

        self.address = Address.objects.create(
            cep_address=fake.postcode(),
            state_address=fake.estado_sigla(),
            city_address=fake.city(),
            district_address=fake.bairro(),
            street_address=fake.street_name(),
            number_address=fake.building_number()
        )

        self.branch = Branch.objects.create(
            name_branch=fake.street_name(),
            opening_hours_start_branch='07:00:00',
            opening_hours_end_branch='17:00:00',
            address_branch=self.address
        )

        self.list_url = reverse('Branches-list')
        self.detail_url = reverse('Branches-detail', kwargs={'pk': self.branch.pk})

    def test_request_to_branch_list(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_branch_creation(self) -> None:
        self.client.force_login(self.user)
        data = {
            'name_branch': 'Branch name',
            'opening_hours_start_branch': '07:00:00',
            'opening_hours_end_branch': '17:00:00',
            'address_branch': self.address,
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_to_branch_detail(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_branch_update(self) -> None:
        self.client.force_login(self.user)
        data = {
            'name_branch': 'Branch name',
            'opening_hours_start_branch': '08:00:00',
            'opening_hours_end_branch': '18:00:00',
            'address_branch': self.address,
        }
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_branch_delete(self) -> None:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

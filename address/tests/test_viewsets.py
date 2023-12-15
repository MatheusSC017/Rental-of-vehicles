from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User, Permission, ContentType
from ..models import Address
from unidecode import unidecode
import faker


class AddressViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.fake = faker.Faker('pt_BR')

        username = self.fake.first_name().replace(' ', '_') + '123456789'
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
            cep=self.fake.postcode(),
            state=self.fake.estado_sigla(),
            city=self.fake.city(),
            district=self.fake.bairro(),
            street=self.fake.street_name(),
            number=self.fake.building_number()
        )

        self.list_url = reverse('Addresses-list')
        self.detail_url = reverse('Addresses-detail', kwargs={'pk': self.address.pk})

    def test_request_to_address_list(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_address_creation(self) -> None:
        self.client.force_login(self.user)
        data = {
            'cep': self.fake.postcode(),
            'state': self.fake.estado_sigla(),
            'city': self.fake.city(),
            'district': self.fake.bairro(),
            'street': self.fake.street_name(),
            'number': self.fake.building_number()
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_to_address_detail(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_address_update(self) -> None:
        self.client.force_login(self.user)
        data = {
            'cep': self.fake.postcode(),
            'state': self.fake.estado_sigla(),
            'city': self.fake.city(),
            'district': self.fake.bairro(),
            'street': self.fake.street_name(),
            'number': self.fake.building_number()
        }
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_address_delete(self) -> None:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

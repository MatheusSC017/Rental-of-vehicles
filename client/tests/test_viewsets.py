from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User, Permission, ContentType
from ..models import Client
from address.models import Address
from random import choice, randrange
from validate_docbr import CPF, CNH
import faker
import copy


class ClientViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.fake = faker.Faker('pt_BR')
        self.cpf = CPF()
        self.cnh = CNH()

        usernames = [self.fake.first_name() + str(randrange(111111, 999999)) for _ in range(3)]
        self.users = [User.objects.create_user(
            username=username,
            email=username + '@email.com',
            password=username
        ) for username in usernames]

        content_type = ContentType.objects.get_for_model(Client)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.users[0].user_permissions.add(permission)

        self.address = Address.objects.create(
            cep_address=self.fake.postcode(),
            state_address=self.fake.estado_sigla(),
            city_address=self.fake.city(),
            district_address=self.fake.bairro(),
            street_address=self.fake.street_name(),
            number_address=self.fake.building_number()
        )

        self.client_user = Client.objects.create(
            cpf_person=self.cpf.generate(),
            rg_person=self.fake.rg(),
            gender_person=choice('MFN'),
            age_person=randrange(18, 60),
            phone_person=self.fake.cellphone_number()[4:],
            address_person=self.address,
            user_client=self.users[1],
            cnh_client=self.cnh.generate(),
            finance_client=randrange(1500, 5000)
        )

        self.data = {
            'cpf_person': self.cpf.generate(),
            'rg_person': self.fake.rg(),
            'gender_person': choice('MFN'),
            'age_person': randrange(18, 60),
            'phone_person': self.fake.cellphone_number()[4:],
            'address_person': self.address.pk,
            'cnh_client': self.cnh.generate(),
            'finance_client': randrange(1500, 5000),
        }

        self.list_url = reverse('Clients-list')
        self.detail_url = reverse('Clients-detail', kwargs={'pk': self.client_user.cpf_person})

    def test_request_to_client_list(self) -> None:
        self.client.force_login(self.users[0])
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_client_creation(self) -> None:
        data = copy.deepcopy(self.data)
        data['user_client'] = self.users[2].pk
        self.client.force_login(self.users[0])
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_request_to_client_detail(self) -> None:
        self.client.force_login(self.users[0])
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_client_update(self) -> None:
        data = copy.deepcopy(self.data)
        data['user_client'] = self.users[1].pk
        data['cpf_person'] = self.client_user.cpf_person
        data['cnh_client'] = self.client_user.cnh_client
        self.client.force_login(self.users[0])
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_client_delete(self) -> None:
        self.client.force_login(self.users[0])
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

from random import choice, randrange
import copy
import faker
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User, Permission, ContentType
from address.models import Address
from validate_docbr import CPF, CNH
from unidecode import unidecode
from ..models import Client


class ClientViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.fake = faker.Faker('pt_BR')
        self.cpf_generator = CPF()
        self.cnh_generator = CNH()

        usernames = [self.fake.first_name().replace(' ', '_') + str(randrange(111111, 999999)) for _ in range(3)]
        self.users_data = [
            {'username': username, 'email': unidecode(username + '@email.com'), 'password': username,
             'first_name': self.fake.first_name(), 'last_name': self.fake.last_name()}
            for username in usernames
        ]
        self.user = User.objects.create_user(
            username=self.users_data[2]['username'],
            email=self.users_data[2]['email'],
            password=self.users_data[2]['password']
        )
        self.users_data.pop()

        content_type = ContentType.objects.get_for_model(Client)
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

        user = User.objects.create_user(
            username=self.users_data[0]['username'],
            email=self.users_data[0]['email'],
            password=self.users_data[0]['password']
        )

        self.client_user = Client.objects.create(
            cpf=self.cpf_generator.generate(),
            rg=self.fake.rg(),
            gender=choice('MFN'),
            age=randrange(18, 60),
            phone=self.fake.cellphone_number()[4:],
            address=self.address,
            user=user,
            cnh=self.cnh_generator.generate(),
            finance=randrange(1500, 5000)
        )

        self.data = {
            'cpf': self.cpf_generator.generate(),
            'rg': self.fake.rg(),
            'gender': choice('MFN'),
            'age': randrange(18, 60),
            'phone': self.fake.cellphone_number()[4:],
            'address': self.address.pk,
            'cnh': self.cnh_generator.generate(),
            'finance': randrange(1500, 5000),
        }

        self.list_url = reverse('Clients-list')
        self.detail_url = reverse('Clients-detail', kwargs={'pk': self.client_user.cpf})

    def test_request_to_client_list(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_client_creation(self) -> None:
        data = copy.deepcopy(self.data)
        data['user'] = self.users_data[1]
        self.client.force_login(self.user)
        response = self.client.post(self.list_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_request_to_client_detail(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_client_update(self) -> None:
        data = copy.deepcopy(self.data)
        data['user'] = self.users_data[1]
        data['cpf'] = self.client_user.cpf
        data['cnh'] = self.client_user.cnh
        self.client.force_login(self.user)
        response = self.client.put(self.detail_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_client_delete(self) -> None:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')

        usernames = [fake.first_name().replace(' ', '_') + str(randrange(11111, 99999)) for _ in range(2)]
        self.users = [User.objects.create_user(
            username=username,
            email=unidecode(username + '@email.com'),
            password=username
        ) for username in usernames]

        content_type = ContentType.objects.get_for_model(User)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.users[0].user_permissions.add(permission)

        self.new_data = {
            'username': 'UsuarioDeTeste',
            'email': 'UsuarioDeTeste@email.com',
            'first_name': 'Usuario',
            'last_name': 'DeTeste',
            'password': 'SenhaTesteUsuario123'
        }

        self.list_url = reverse('Users-list')
        self.detail_url = reverse('Users-detail', kwargs={'pk': self.users[1].pk})

    def test_request_to_user_list_with_anonymous_user(self) -> None:
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_request_to_user_list(self) -> None:
        self.client.force_login(self.users[0])
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_test_request_to_user_creation(self) -> None:
        self.client.force_login(self.users[0])
        response = self.client.post(self.list_url, data=self.new_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_request_to_user_detail(self) -> None:
        self.client.force_login(self.users[0])
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_to_user_update(self) -> None:
        data = copy.deepcopy(self.new_data)
        data['username'] = self.users[1].username
        self.client.force_login(self.users[0])
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_request_to_user_delete(self) -> None:
        self.client.force_login(self.users[0])
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

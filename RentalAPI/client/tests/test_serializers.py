from random import choice, randrange
import faker
from django.test import TestCase
from django.contrib.auth.models import User
from address.models import Address
from utils.mixins.serializers import GetRelationOfTheFieldMixin
from validate_docbr import CNH
from unidecode import unidecode
from ..serializers import ClientSerializer, UserSerializer
from ..models import Client


class ClientSerializerTestCase(TestCase, GetRelationOfTheFieldMixin):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')
        cnh_generator = CNH()

        username = fake.first_name().replace(' ', '_') + '123456789'
        user = User.objects.create_user(
            username=username,
            email=unidecode(username + '@email.com'),
            password=username
        )

        address = Address.objects.create(
            cep=fake.postcode(),
            state=fake.estado_sigla(),
            city=fake.city(),
            district=fake.bairro(),
            street=fake.street_name(),
            number=fake.building_number()
        )

        self.client = Client.objects.create(
            cpf=fake.ssn(),
            rg=fake.rg(),
            gender=choice('MFN'),
            age=randrange(18, 80),
            phone=fake.cellphone_number()[4:],
            address=address,
            user=user,
            cnh=cnh_generator.generate(),
            finance=randrange(1500, 5000)
        )

        self.keys = {'cpf', 'rg', 'gender', 'age', 'phone', 'address', 'user', 'cnh', 'finance', }

        self.serializer = ClientSerializer(self.client)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), self.keys)

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        for key in self.keys:
            _, objects = self.get_many_to_many_and_objects_fields(Client)
            if key in objects:
                self.assertEqual(data[key], getattr(self.client, key).id)
            else:
                self.assertEqual(data[key], getattr(self.client, key))


class UserSerializerTestCase(TestCase):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')

        username = fake.first_name().replace(' ', '_') + str(randrange(11111, 99999))
        self.user = User.objects.create_user(
            username=username,
            email=unidecode(username + '@email.com'),
            password=username
        )

        self.keys = {'pk', 'username', 'email', 'first_name', 'last_name'}

        self.serializer = UserSerializer(self.user)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), self.keys)

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        for key in self.keys:
            self.assertEqual(data[key], getattr(self.user, key))

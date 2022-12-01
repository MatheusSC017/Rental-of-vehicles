from django.test import TestCase
from ..serializers import ClientSerializer
from django.contrib.auth.models import User
from ..models import Client
from address.models import Address
from utils.mixins.serializers import GetRelationOfTheFieldMixin
from random import choice, randrange
from validate_docbr import CNH
import faker


class ClientSerializerTestCase(TestCase, GetRelationOfTheFieldMixin):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')
        cnh = CNH()

        username = fake.first_name() + '123456789'
        user = User.objects.create_user(
            username=username,
            email=username + '@email.com',
            password=username
        )

        address = Address.objects.create(
            cep_address=fake.postcode(),
            state_address=fake.estado_sigla(),
            city_address=fake.city(),
            district_address=fake.bairro(),
            street_address=fake.street_name(),
            number_address=fake.building_number()
        )

        self.client = Client.objects.create(
            cpf_person=fake.ssn(),
            rg_person=fake.rg(),
            gender_person=choice('MFN'),
            age_person=randrange(18, 80),
            phone_person=fake.cellphone_number()[4:],
            address_person=address,
            user_client=user,
            cnh_client=cnh.generate(),
            finance_client=randrange(1500, 5000)
        )

        self.keys = {'cpf_person', 'rg_person', 'gender_person', 'age_person', 'phone_person', 'address_person',
                     'user_client', 'cnh_client', 'finance_client', }

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

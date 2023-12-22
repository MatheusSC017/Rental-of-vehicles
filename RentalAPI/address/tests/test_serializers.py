import faker
from django.test import TestCase
from ..serializers import AddressSerializer
from ..models import Address


class AddressSerializerTestCase(TestCase):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')

        self.address = Address.objects.create(
            cep=fake.postcode(),
            state=fake.estado_sigla(),
            city=fake.city(),
            district=fake.bairro(),
            street=fake.street_name(),
            number=fake.building_number()
        )

        self.keys = {'id', 'cep', 'state', 'city', 'district', 'street',
                     'number', }

        self.serializer = AddressSerializer(self.address)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), self.keys)

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        for key in self.keys:
            self.assertEqual(data[key], getattr(self.address, key))

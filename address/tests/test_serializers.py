from django.test import TestCase
from ..serializers import AddressSerializer
from ..models import Address
import faker


class AddressSerializerTestCase(TestCase):
    def setUp(self) -> None:
        fake = faker.Faker('pt_BR')

        self.address = Address.objects.create(
            cep_address=fake.postcode(),
            state_address=fake.estado_sigla(),
            city_address=fake.city(),
            district_address=fake.bairro(),
            street_address=fake.street_name(),
            number_address=fake.building_number()
        )

        self.keys = {'id', 'cep_address', 'state_address', 'city_address', 'district_address', 'street_address',
                     'number_address', }

        self.serializer = AddressSerializer(self.address)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), self.keys)

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        for key in self.keys:
            self.assertEqual(data[key], getattr(self.address, key))

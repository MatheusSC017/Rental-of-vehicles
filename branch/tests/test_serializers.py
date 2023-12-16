import faker
from django.test import TestCase
from django.db.models import Count
from address.models import Address
from ..serializers import BranchSerializer
from ..models import Branch


class BranchSerializerTestCase(TestCase):
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

        self.branch = Branch.objects.create(
            name=fake.street_name(),
            opening_hours_start='07:00:00',
            opening_hours_end='17:00:00',
            address=self.address
        )

        self.serializer = BranchSerializer(Branch.objects.annotate(number_vehicles=Count('vehicle'))[0])

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'pk', 'name', 'opening_hours_start',
                                            'opening_hours_end', 'address_info', 'number_vehicles'})

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(data['name'], self.branch.name)
        self.assertEqual(data['opening_hours_start'], self.branch.opening_hours_start)
        self.assertEqual(data['opening_hours_end'], self.branch.opening_hours_end)
        self.assertEqual(data['address_info'], str(self.address))
        self.assertEqual(data['number_vehicles'], 0)

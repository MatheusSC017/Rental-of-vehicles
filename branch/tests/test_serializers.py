from django.test import TestCase
from django.db.models import Count
from ..serializers import BranchSerializer
from ..models import Branch
from address.models import Address
import faker


class BranchSerializerTestCase(TestCase):
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

        self.branch = Branch.objects.create(
            name_branch=fake.street_name(),
            opening_hours_start_branch='07:00:00',
            opening_hours_end_branch='17:00:00',
            address_branch=self.address
        )

        self.serializer = BranchSerializer(Branch.objects.annotate(number_vehicles=Count('vehicle'))[0])

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'pk', 'name_branch', 'opening_hours_start_branch',
                                            'opening_hours_end_branch', 'address_info', 'number_vehicles'})

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(data['name_branch'], self.branch.name_branch)
        self.assertEqual(data['opening_hours_start_branch'], self.branch.opening_hours_start_branch)
        self.assertEqual(data['opening_hours_end_branch'], self.branch.opening_hours_end_branch)
        self.assertEqual(data['address_info'], str(self.address))
        self.assertEqual(data['number_vehicles'], 0)

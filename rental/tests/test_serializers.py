from django.test import TestCase
from ..models import Insurance, AdditionalItems
from ..serializers import InsuranceSerializer, AdditionalItemsSerializer
import json


class InsuranceSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.insurance = Insurance.objects.create(
            title_insurance='InsuranceTitle',
            coverage_insurance=json.dumps({'Coverage': 100000., 'Steal': 30000.}),
            price_insurance=5.
        )
        self.serializer = InsuranceSerializer(instance=self.insurance)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title_insurance', 'coverage_insurance', 'price_insurance']))

    def test_verify_serializer_fields_content(self) -> None:
        data = self.serializer.data
        self.assertEqual(data['title_insurance'], self.insurance.title_insurance)
        self.assertEqual(data['coverage_insurance'], self.insurance.coverage_insurance)
        self.assertEqual(data['price_insurance'], self.insurance.price_insurance)

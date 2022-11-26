from django.test import TestCase
from ..models import VehicleClassification, Vehicle
from ..serializers import VehicleClassificationSerializer, VehicleSerializer, VehicleSerializerV2


class VehicleClassificationSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.classification = VehicleClassification.objects.create(
            title_classification='Vehicle Classification',
            daily_cost_classification=7.5
        )
        self.serializer = VehicleClassificationSerializer(self.classification)

    def test_verify_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title_classification', 'daily_cost_classification', ]))

    def test_verify_contents_of_serializer_fields(self) -> None:
        data = self.serializer.data
        self.assertEqual(data['title_classification'], self.classification.title_classification)
        self.assertEqual(data['daily_cost_classification'], self.classification.daily_cost_classification)

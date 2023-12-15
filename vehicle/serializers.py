from rest_framework.serializers import ModelSerializer
from .models import Vehicle, VehicleClassification


class VehicleClassificationSerializer(ModelSerializer):
    class Meta:
        model = VehicleClassification
        fields = '__all__'


class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['type', 'brand', 'model', 'year_manufacture',
                  'model_year', 'mileage', 'renavam', 'license_plate',
                  'chassi', 'fuel', 'fuel_tank', 'engine', 'color',
                  'other_data', 'available', 'branch', 'classification', ]


class VehicleSerializerV2(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

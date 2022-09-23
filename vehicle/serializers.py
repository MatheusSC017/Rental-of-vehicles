from rest_framework.serializers import ModelSerializer
from .models import Vehicle


class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['type_vehicle', 'brand_vehicle', 'model_vehicle', 'year_manufacture_vehicle',
                  'model_year_vehicle', 'mileage_vehicle', 'renavam_vehicle', 'license_plate_vehicle',
                  'chassi_vehicle', 'fuel_vehicle', 'fuel_tank_vehicle', 'engine_vehicle', 'color_vehicle',
                  'other_data_vehicle', 'available_vehicle', 'branch_vehicle', 'classification_vehicle', ]


class VehicleSerializerV2(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

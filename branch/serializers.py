from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Branch


class BranchSerializer(ModelSerializer):
    number_vehicles = IntegerField()

    class Meta:
        model = Branch
        fields = ['pk', 'name_branch', 'opening_hours_start_branch', 'opening_hours_end_branch',
                  'address_branch', 'number_vehicles', ]
        read_only_fields = ['number_vehicles', ]

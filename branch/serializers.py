from rest_framework.serializers import ModelSerializer, IntegerField, CharField
from .models import Branch


class BranchSerializer(ModelSerializer):
    number_vehicles = IntegerField(read_only=True)
    address_info = CharField(read_only=True)

    class Meta:
        model = Branch
        fields = ['pk', 'name_branch', 'opening_hours_start_branch', 'opening_hours_end_branch',
                  'address_info', 'number_vehicles', ]

from rest_framework.serializers import ModelSerializer
from .models import StaffMember


class StaffSerializer(ModelSerializer):
    class Meta:
        model = StaffMember
        fields = ['user', 'salary', 'branch', ]

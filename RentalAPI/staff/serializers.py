from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import StaffMember


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email', 'password', ]


class StaffSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StaffMember
        fields = ['user', 'salary', 'branch', ]

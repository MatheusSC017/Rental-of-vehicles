from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Client


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email', 'password', ]
        extra_kwargs = {'password': {'write_only': True}}


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['cpf', 'rg', 'gender', 'age', 'phone', 'address', 'user', 'cnh', 'finance', ]


class ClientReadOnlySerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['cpf', 'rg', 'gender', 'age', 'phone', 'address', 'user', 'cnh', 'finance', ]

from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Client


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email', 'password', ]
        extra_kwargs = {'password': {'write_only': True}}

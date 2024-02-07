from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.db import transaction
from .models import Client


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email', 'password', ]
        extra_kwargs = {'password': {'write_only': True}}


class ClientSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = ['cpf', 'rg', 'gender', 'age', 'phone', 'address', 'user', 'cnh', 'finance', ]

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = User.objects.create_user(**user_data)

        client = Client.objects.create(user=user, **validated_data)

        return client

    @transaction.atomic
    def update(self, instance, validated_data):
        user_instance = instance.user
        user_data = validated_data.pop('user')

        for attr, value in user_data.items():
            setattr(user_instance, attr, value)

        user_instance.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .models import Client
from .serializers import ClientSerializer, UserSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer



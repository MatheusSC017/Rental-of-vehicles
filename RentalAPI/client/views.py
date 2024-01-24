from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .models import Client
from .serializers import ClientSerializer, ClientReadOnlySerializer, UserSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ClientReadOnlySerializer
        return ClientSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer

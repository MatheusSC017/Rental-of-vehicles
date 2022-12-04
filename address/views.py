from rest_framework.viewsets import ModelViewSet
from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

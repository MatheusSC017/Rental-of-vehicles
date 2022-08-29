from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from address.models import Address
from address.serializers import AddressSerializer
from vehicle.models import Vehicle
from vehicle.serializers import VehicleSerializer
from .models import Branch
from .serializers import BranchSerializer


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class BranchAddressViewSet(ReadOnlyModelViewSet):
    addresses = [b.address_branch.pk for b in Branch.objects.all()]
    queryset = Address.objects.filter(pk__in=addresses)
    serializer_class = AddressSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class BranchVehicleViewSet(ReadOnlyModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        branch = self.kwargs.get('branch')

        qs = Vehicle.objects.filter(branch_vehicle=branch)

        return qs

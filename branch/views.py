from rest_framework.viewsets import ModelViewSet, generics
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from django.db.models import Count
from address.models import Address
from address.serializers import AddressSerializer
from vehicle.models import Vehicle
from vehicle.serializers import VehicleSerializer
from .models import Branch
from .serializers import BranchSerializer


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.annotate(number_vehicles=Count('vehicle'))
    serializer_class = BranchSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BranchAddressViewSet(generics.ListAPIView):
    """
    addresses = [b.address_branch.pk for b in Branch.objects.all()]
    queryset = Address.objects.filter(pk__in=addresses)
    """
    serializer_class = AddressSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        branch = Branch.objects.filter(pk=pk)[0]
        qs = Address.objects.filter(pk=branch.address_branch.pk)
        return qs


class BranchVehicleViewSet(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        qs = Vehicle.objects.filter(branch_vehicle=pk)
        return qs

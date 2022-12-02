from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
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

    @method_decorator(cache_page(60 * 60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BranchAddressViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = AddressSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    http_method_names = ['get', ]

    @method_decorator(cache_page(60 * 60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        branch = Branch.objects.filter(pk=pk)[0]
        qs = Address.objects.filter(pk=branch.address_branch.pk)
        return qs


class BranchVehicleViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    http_method_names = ['get', ]

    @method_decorator(cache_page(60 * 60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if self.request.query_params.get('show_all'):
            return Vehicle.objects.filter(branch_vehicle=pk)
        return Vehicle.objects.filter(branch_vehicle=pk, available_vehicle=True)

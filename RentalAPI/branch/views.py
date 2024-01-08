from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions
from django.conf import settings
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from address.models import Address
from address.serializers import AddressSerializer
from vehicle.models import Vehicle
from vehicle.serializers import VehicleSerializer
from staff.models import StaffMember
from staff.serializers import StaffSerializer
from rental.models import AdditionalItems
from rental.serializers import AdditionalItemsSerializer
from .models import Branch
from .serializers import BranchSerializer


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.annotate(number_vehicles=Count('vehicle'))
    serializer_class = BranchSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @method_decorator(cache_page(settings.CACHE_PAGE_DURATION))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BranchAddressViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = AddressSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    http_method_names = ['get', ]

    @method_decorator(cache_page(settings.CACHE_PAGE_DURATION))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        branch = Branch.objects.filter(pk=pk)[0]
        qs = Address.objects.filter(pk=branch.address.pk)
        return qs


class BranchVehicleViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    http_method_names = ['get', ]

    @method_decorator(cache_page(settings.CACHE_PAGE_DURATION))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if self.request.query_params.get('show_available'):
            return Vehicle.objects.filter(branch=pk, available=True)
        return Vehicle.objects.filter(branch=pk)


class BranchAdditionalItemsViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = AdditionalItemsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    http_method_names = ['get', ]

    @method_decorator(cache_page(settings.CACHE_PAGE_DURATION))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return AdditionalItems.objects.filter(branch=pk)


class BranchStaffViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = StaffSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', ]

    @method_decorator(cache_page(settings.CACHE_PAGE_DURATION))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return StaffMember.objects.filter(branch=pk)

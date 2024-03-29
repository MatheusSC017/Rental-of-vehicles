from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Vehicle, VehicleClassification
from .serializers import VehicleSerializer, VehicleSerializerV2, VehicleClassificationSerializer


class VehicleClassificationViewSet(ModelViewSet):
    queryset = VehicleClassification.objects.all()
    serializer_class = VehicleClassificationSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]

    @method_decorator(cache_page(settings.CACHE_PAGE_DURATION))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class VehicleViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]

    @method_decorator(cache_page(settings.CACHE_PAGE_DURATION))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.query_params.get('show_available'):
            return Vehicle.objects.filter(available=True)
        return Vehicle.objects.all()

    def get_serializer_class(self):
        """ By default the latest version is chosen if no version is specified """
        if self.request.version == 'v1':
            return VehicleSerializer
        return VehicleSerializerV2

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Vehicle, VehicleClassification
from .serializers import VehicleSerializer, VehicleSerializerV2, VehicleClassificationSerializer


class VehicleClassificationViewSet(ModelViewSet):
    queryset = VehicleClassification.objects.all()
    serializer_class = VehicleClassificationSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]

    @method_decorator(cache_page(60 * 60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]

    @method_decorator(cache_page(60 * 60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        """ By default the latest version is chosen if no version is specified """
        if self.request.version == 'v1':
            return VehicleSerializer
        else:
            return VehicleSerializerV2

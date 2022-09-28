from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Vehicle
from .serializers import VehicleSerializer, VehicleSerializerV2


class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]

    @method_decorator(cache_page(30))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        """ By default the latest version is chosen if no version is specified """
        if self.request.version == 'v1':
            return VehicleSerializer
        else:
            return VehicleSerializerV2

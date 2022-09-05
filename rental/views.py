from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from vehicle.models import Vehicle
from .permissions import OnlyStaffMemberPermission
from .serializers import InsuranceSerializer, RentalSerializer
from .models import Insurance, Rental


class InsuranceViewSet(ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]


class RentalViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [OnlyStaffMemberPermission, ]

    def perform_create(self, request, serializer):
        vehicle = get_object_or_404(Vehicle, renavam_vehicle=request.data.get('vehicle_rental'))
        serializer.save(
            staff_rental=request.user.staffmember,
            daily_cost_rental=vehicle.classification_vehicle.daily_cost_classification
        )

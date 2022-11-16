from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from vehicle.models import Vehicle
from .permissions import OnlyStaffMemberPermission
from .serializers import InsuranceSerializer, AdditionalItemsSerializer, RentalSerializer
from .models import Insurance, AdditionalItems, Rental


class InsuranceViewSet(ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]


class AdditionalItemsViewSet(ModelViewSet):
    queryset = AdditionalItems.objects.all()
    serializer_class = AdditionalItemsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]


class RentalViewSet():
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [OnlyStaffMemberPermission, ]
    http_method_names = ['get', 'post', 'put', 'path', ]

    def perform_create(self, serializer):
        vehicle = get_object_or_404(Vehicle, renavam_vehicle=self.request.data.get('vehicle_rental'))
        serializer.save(
            staff_rental=self.request.user.staffmember,
            outlet_branch_rental=vehicle.branch_vehicle,
            daily_cost_rental=vehicle.classification_vehicle.daily_cost_classification,
        )

    def perform_update(self, serializer):
        vehicle = get_object_or_404(Vehicle, renavam_vehicle=self.request.data.get('vehicle_rental'))
        serializer.save(
            daily_cost_rental=vehicle.classification_vehicle.daily_cost_classification,
            outlet_branch_rental=vehicle.branch_vehicle,
        )

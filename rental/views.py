from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from vehicle.models import Vehicle
from .permissions import OnlyStaffMemberPermission
from .serializers import InsuranceSerializer, RentalSerializer
from .models import Insurance, Rental
from .validators import valid_appointment_update_or_cancellation
from datetime import date


class InsuranceViewSet(ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]


class RentalViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [OnlyStaffMemberPermission, ]

    def perform_create(self, serializer):
        vehicle = get_object_or_404(Vehicle, renavam_vehicle=self.request.data.get('vehicle_rental'))
        rent_date_rental = date.today() if self.request.data.get('status_rental') == 'L' else None

        serializer.save(
            staff_rental=self.request.user.staffmember,
            outlet_branch_rental=vehicle.branch_vehicle,
            daily_cost_rental=vehicle.classification_vehicle.daily_cost_classification,
            rent_date_rental=rent_date_rental
        )

    def perform_update(self, serializer):
        vehicle = get_object_or_404(Vehicle, renavam_vehicle=self.request.data.get('vehicle_rental'))
        daily_cost = vehicle.classification_vehicle.daily_cost_classification
        if not valid_appointment_update_or_cancellation(self.request.data.get('appointment_date_rental')):
            fines_rental = self.calculate_fines(daily_cost)
        else:
            fines_rental = None
        rent_date_rental = date.today() if self.request.data.get('status_rental') == 'L' else None

        serializer.save(
            daily_cost_rental=daily_cost,
            outlet_branch_rental=vehicle.branch_vehicle,
            rent_date_rental=rent_date_rental,
            fines_rental=fines_rental
        )

    def calculate_fines(self, daily_cost):
        total_daily_cost = float(daily_cost) + float(self.request.data.get('additional_daily_cost_rental'))
        return round(float(self.request.data.get('requested_days_rental')) * total_daily_cost * 0.2, 2)

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


class RentalViewSet(ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [OnlyStaffMemberPermission, ]
    http_method_names = ['get', 'post', 'put', 'path', ]

    def perform_create(self, serializer):
        serializer.save(
            staff_rental=self.request.user.staffmember,
            **self.fetch_values_to_fill_fields()
        )

    def perform_update(self, serializer):
        serializer.save(**self.fetch_values_to_fill_fields())

    def fetch_values_to_fill_fields(self) -> dict:
        branch = self.request.user.staffmember.branch_staffmember
        vehicle = get_object_or_404(Vehicle,
                                    renavam_vehicle=self.request.data.get('vehicle_rental'),
                                    branch_vehicle=branch)
        return {
            'daily_cost_rental': vehicle.classification_vehicle.daily_cost_classification,
            'outlet_branch_rental': vehicle.branch_vehicle,
            'additional_daily_cost_rental': self.calculate_additional_daily_cost()
        }

    def calculate_additional_daily_cost(self) -> float:
        try:
            pk_addional_items_list = [int(additional_item) for additional_item
                                      in dict(self.request.data).get('additional_items_rental')]
            additional_items_list = AdditionalItems.objects.filter(pk__in=pk_addional_items_list)
            return sum([additional_item.daily_cost_additionalitems for additional_item in additional_items_list])
        except TypeError:
            return 0.

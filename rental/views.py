from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
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
            # Get the list of additional items requested
            relationship_additional_items_list = [additional_item for additional_item
                                                  in dict(self.request.data).get('additional_items_rental')]
            # The next step will be to create a list with the subtotal for each additional item
            additional_items_list = (
                AdditionalItems.objects.filter(pk=item['additional_item_relationship'])[0].daily_cost_additionalitems *
                item['number_relationship']
                for item in relationship_additional_items_list
            )
            return sum(additional_items_list)
        except TypeError:
            return 0.


@api_view(['GET', ])
@permission_classes([OnlyStaffMemberPermission, ])
def late_appointments(request):
    queryset = Rental.objects.filter(status_rental='A', appointment_date_rental__lt=str(timezone.now())[:10])
    return Response(data=RentalSerializer(queryset, many=True).data)

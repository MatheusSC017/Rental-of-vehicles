from django.shortcuts import get_object_or_404
from django.db.models.expressions import RawSQL
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from vehicle.models import Vehicle
from .permissions import OnlyStaffMemberPermission
from .serializers import (
    InsuranceSerializer,
    AdditionalItemsSerializer,
    RentalSerializer,
    AppointmentSerializer,
    RentCreateSerializer,
    RentUpdateSerializer
)
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
            staff=self.request.user.staffmember,
            **self.fetch_values_to_fill_fields()
        )

    def perform_update(self, serializer):
        serializer.save(**self.fetch_values_to_fill_fields())

    def fetch_values_to_fill_fields(self) -> dict:
        """ fetch the values for fields with autocomplete """
        vehicle = get_object_or_404(Vehicle, renavam=self.request.data.get('vehicle'))
        return {
            'daily_cost': vehicle.classification.daily_cost,
            'outlet_branch': vehicle.branch,
            'additional_daily_cost': self.calculate_additional_daily_cost()
        }

    def calculate_additional_daily_cost(self) -> float:
        """ Calculate de total additional daily cost
        The total daily additional cost will be calculated based on the additional items received in the request,
        returning the sum of the subtotals (cost of additional item times quantity) of each additional item
        """
        try:
            # Get the list of additional items requested
            relationship_additional_items_list = list(dict(self.request.data).get('additional_items'))
            # The next step will be to create a list with the subtotal for each additional item
            additional_items_list = (
                AdditionalItems.objects.filter(pk=item['additional_item'])[0].daily_cost * item['number']
                for item in relationship_additional_items_list
            )
            return sum(additional_items_list)
        except TypeError:
            return 0.


class GenericRentalCreateViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Rental.objects.all()
    permission_classes = [OnlyStaffMemberPermission, ]
    http_method_names = ['post', 'put' ]

    def perform_create(self, serializer):
        serializer.save(
            staff=self.request.user.staffmember,
            **self.fetch_values_to_fill_fields()
        )

    def perform_update(self, serializer):
        serializer.save(
            staff=self.request.user.staffmember,
            **self.fetch_values_to_fill_fields()
        )

    def fetch_values_to_fill_fields(self) -> dict:
        """ fetch the values for fields with autocomplete """
        vehicle = get_object_or_404(Vehicle, renavam=self.request.data.get('vehicle'))
        return {
            'daily_cost': vehicle.classification.daily_cost,
            'outlet_branch': vehicle.branch,
            'additional_daily_cost': self.calculate_additional_daily_cost()
        }

    def calculate_additional_daily_cost(self) -> float:
        """ Calculate de total additional daily cost
        The total daily additional cost will be calculated based on the additional items received in the request,
        returning the sum of the subtotals (cost of additional item times quantity) of each additional item
        """
        try:
            # Get the list of additional items requested
            relationship_additional_items_list = list(dict(self.request.data).get('additional_items'))
            # The next step will be to create a list with the subtotal for each additional item
            additional_items_list = (
                AdditionalItems.objects.filter(pk=item['additional_item'])[0].daily_cost * item['number']
                for item in relationship_additional_items_list
            )
            return sum(additional_items_list)
        except TypeError:
            return 0.


class AppointmentCreateUpdateViewSet(GenericRentalCreateViewSet):
    serializer_class = AppointmentSerializer


class RentalCreateUpdateViewSet(GenericRentalCreateViewSet):
    http_method_names = ['post', 'put', ]

    def get_serializer_class(self):
        if self.action == 'create':
            return RentCreateSerializer
        elif self.action == 'update':
            return RentUpdateSerializer
        return RentCreateSerializer


@api_view(['GET', ])
@permission_classes([OnlyStaffMemberPermission, ])
def late_appointments(request):
    queryset = Rental.objects.filter(status='A', appointment_date__lt=str(timezone.now())[:10])
    return Response(data=RentalSerializer(queryset, many=True).data)


@api_view(['GET', ])
@permission_classes([OnlyStaffMemberPermission, ])
def late_devolutions(request):
    queryset = Rental.objects.annotate(
        devolution_date_expected=RawSQL('DATE_ADD(appointment_date, INTERVAL requested_days DAY)', ()),
    ).filter(status='D', devolution_date_expected__lt=str(timezone.now())[:10])
    return Response(data=RentalSerializer(queryset, many=True).data)

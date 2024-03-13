import json
from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models.expressions import RawSQL
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated
from rest_framework.response import Response
from vehicle.models import Vehicle
from .auth import MessagingSystemAccessTokenAuthentication
from .permissions import OnlyStaffMemberPermission
from .serializers import (
    InsuranceSerializer,
    AdditionalItemsSerializer,
    RentalSerializer,
    AppointmentSerializer,
    RentCreateSerializer,
    RentUpdateSerializer,
    AppointmentMessageSerializer,
    LateDevolutionMessageSerializer,
)
from branch.models import Branch
from .models import Insurance, AdditionalItems, Rental
from .utils import inventory_update_for_rental_devolution_or_cancellation, get_distance_of_return


class InsuranceViewSet(ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]


class AdditionalItemsViewSet(ModelViewSet):
    queryset = AdditionalItems.objects.all()
    serializer_class = AdditionalItemsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]


class RentalViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [OnlyStaffMemberPermission, ]
    http_method_names = ['get', ]


class GenericRentalCreateViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Rental.objects.all()
    permission_classes = [OnlyStaffMemberPermission, ]
    http_method_names = ['post', 'put']

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
        if self.action == 'update':
            return RentUpdateSerializer
        return RentCreateSerializer


@api_view(['PUT', ])
@permission_classes([OnlyStaffMemberPermission, ])
def appointment_to_rent_update(request, pk):
    rent = get_object_or_404(Rental, id=pk)
    if rent.status != 'A':
        return Response(data=json.dumps(_('You can only move an appointment to the rental state')))
    rent.status = 'L'
    rent.save()
    return Response(data=RentalSerializer(rent).data)


@api_view(['PUT', ])
@permission_classes([OnlyStaffMemberPermission, ])
@transaction.atomic
def cancel_appointment(request, pk):
    rent = get_object_or_404(Rental, id=pk)
    if rent.status != 'A':
        return Response(data=json.dumps("You can only can cancel a register with appointment state"))
    rent.status = 'C'
    rent.save()
    inventory_update_for_rental_devolution_or_cancellation(rent)
    return Response(data=RentalSerializer(rent).data)


@api_view(['PUT', ])
@permission_classes([OnlyStaffMemberPermission, ])
@transaction.atomic
def vehicle_devolution(request, pk):
    rent = get_object_or_404(Rental, id=pk)

    if rent.status != 'L':
        return Response(data=json.dumps("You can only return a vehicle for rental registration in allocation states"))

    arrival_branch = request.data.get('arrival_branch')
    if arrival_branch:
        arrival_branch = Branch.objects.get(id=arrival_branch)
        distance_branch = get_distance_of_return(rent.outlet_branch.address, arrival_branch.address)
        rent.arrival_branch = arrival_branch
        rent.distance_branch = distance_branch

    rent.status = 'D'
    rent.save()
    inventory_update_for_rental_devolution_or_cancellation(rent)
    return Response(data=RentalSerializer(rent).data)


@api_view(['GET', ])
@permission_classes((OnlyStaffMemberPermission,))
def late_appointments(request):
    queryset = Rental.objects.filter(status='A', appointment_date__lt=str(timezone.now())[:10])
    return Response(data=RentalSerializer(queryset, many=True).data)


@api_view(['GET', ])
@permission_classes((OnlyStaffMemberPermission,))
def late_devolutions(request):
    queryset = Rental.objects.annotate(
        devolution_date_expected=RawSQL('DATE_ADD(appointment_date, INTERVAL requested_days DAY)', ()),
    ).filter(status='L', devolution_date_expected__lt=str(timezone.now())[:10])
    return Response(data=RentalSerializer(queryset, many=True).data)


@api_view(['GET', ])
@authentication_classes([MessagingSystemAccessTokenAuthentication, ])
@permission_classes((IsAuthenticated,))
def messages_late_appointment(request):
    queryset = Rental.objects.annotate(subject=models.Value('late_appointment', output_field=models.CharField())). \
        filter(status='A', appointment_date__lt=str(timezone.now())[:10])
    return Response(data=AppointmentMessageSerializer(queryset, many=True).data)


@api_view(['GET', ])
@authentication_classes([MessagingSystemAccessTokenAuthentication, ])
@permission_classes((IsAuthenticated,))
def messages_late_devolution(request):
    queryset = Rental.objects.annotate(
        devolution_date_expected=RawSQL('DATE_ADD(appointment_date, INTERVAL requested_days DAY)', ()),
    ).annotate(subject=models.Value('late_devolution', output_field=models.CharField())).\
        filter(status='L', devolution_date_expected__lt=str(timezone.now())[:10])

    return Response(data=LateDevolutionMessageSerializer(queryset, many=True).data)


@api_view(['GET', ])
@authentication_classes([MessagingSystemAccessTokenAuthentication, ])
@permission_classes((IsAuthenticated,))
def messages_appointment(request):
    queryset = Rental.objects.annotate(
        subject=models.Value('late_appointment', output_field=models.CharField())
    ).annotate(
        appointment_date_notices=RawSQL('DATE_SUB(appointment_date, INTERVAL 5 DAY)', ()),
    ).filter(
        status='A',
        appointment_date_notices__lt=str(timezone.now())[:10],
        appointment_date__gt=str(timezone.now())[:10]
    )
    return Response(data=AppointmentMessageSerializer(queryset, many=True).data)

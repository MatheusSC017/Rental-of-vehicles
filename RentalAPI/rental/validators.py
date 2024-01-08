from datetime import datetime, timedelta
from typing import Any
from rest_framework.utils import model_meta
from django.db.models import Q
from django.db.models.expressions import RawSQL
from django.utils import timezone
import rental.models as rental_models

STATUS_UPDATE = {
    'A': ('A', 'L', 'C'),
    'L': ('L', 'D',),
    'C': ('C',),
    'D': ('D',),
}

ALLOW_FIELD_UPDATE = {
    'A': ('vehicle', 'insurance', 'status', 'appointment_date', 'requested_days',
          'rent_deposit', 'driver', 'additional_items', 'additional_daily_cost', ),
    'L': ('status', 'driver', ),
    'C': ('status',),
    'D': ('status', 'arrival_branch',),
}

TOLERANCE_DAYS = 3


def valid_rental_states_on_create(status_rental) -> bool:
    """
    Check the initial status allowed
    :param status_rental: A letter indicating the status of the rent
    :return: A boolean indicating if the status on create of the rent is valid or not
    """
    return status_rental in ('A', 'L')


def valid_rental_states_on_update(old_status_rental, new_status_rental) -> bool:
    """
    Validates if the required status transition is allowed
    :param old_status_rental: This field get the current status of the rent
    :param new_status_rental: This field get the new status of the rent
    :return: A boolean indicating if the status transition is valid or not
    """
    return new_status_rental in STATUS_UPDATE[old_status_rental]


def valid_rental_data_update(instance, validated_data) -> tuple[bool, Any]:
    """
    This validation verifies that only the allowed fields are updated, to ensure that the rest of the fields
    (autocomplete or post-completion) remain unchanged
    :param instance: An instance of the rental model class
    :param validated_data: A dictionary with the new values of the fields
    :return: Returns two values, the first is a boolean which is True if updates are accepted or False otherwise.
    The second value is a list of allowed fields to update
    """
    status_rental = validated_data.get('status')

    # Select the many-to-many fields
    info = model_meta.get_field_info(rental_models.Rental)
    many_to_many = []
    for field_name, relation_info in info.relations.items():
        if relation_info.to_many and field_name not in ALLOW_FIELD_UPDATE[status_rental]:
            many_to_many.append(field_name)

    # Checks if the read-only fields have been modified
    disallow_field_update = validated_data.keys() - ALLOW_FIELD_UPDATE[status_rental]
    response = True

    for field in disallow_field_update:
        if field in many_to_many:
            equal_values = list(instance.driver.all()) == validated_data.get('driver')
            if not equal_values:
                response = False
        else:
            if getattr(instance, field) != validated_data.get(field):
                response = False

    return response, ALLOW_FIELD_UPDATE[status_rental]


def valid_appointment_creation(appointment_date) -> bool:
    """
    Validates if the appointment date chosen is valid, that is, greater than today and less than today plus one year
    :param appointment_date: A string indicating the appointment date chosen
    :return: True if the appointment date is valid and False otherwise
    """
    if not appointment_date:
        return False

    appointment_date = timezone.make_aware(datetime.strptime(str(appointment_date), '%Y-%m-%d'))
    now = timezone.make_aware(datetime.strptime(str(timezone.now())[:10], '%Y-%m-%d'))
    if appointment_date <= now:
        return False

    if appointment_date > (now + timezone.timedelta(days=365)):
        return False

    return True


def valid_rented_vehicle(renavam_vehicle, requested_days, id_rental=None) -> bool:
    """
    Check that the rental date coincides a rental or appointment for the same vehicle
    :param renavam_vehicle: A string indicating the value of the vehicle's renavam
    :param requested_days: A positive integer for represents the number of days required
    :param id_rental: If you need to validate a rental update, you must provide the rental id for exclude it of the
    search
    :return: return True if the rental not match other rentals or appointments and False otherwise
    """
    # Check if there are rentals with the status of rented
    rented = Q(status='L')
    # Check for scheduled rentals within the new rental schedule plus 3 days
    initial_date = Q(
        Q(status__in=('A', 'L')),
        Q(appointment_date__gte=timezone.now()),
        Q(appointment_date__lte=timezone.now() + timezone.timedelta(days=requested_days + TOLERANCE_DAYS))
    )
    rentals = rental_models.Rental.objects.filter(
        Q(vehicle=renavam_vehicle),
        rented |
        initial_date
    )

    if id_rental:
        return not rentals.exclude(id=id_rental)

    return not rentals


def valid_scheduled_vehicle(renavam, appointment_date, requested_days, id_rental=None) -> bool:
    """
    Check that the appointment date coincides a rental or appointment for the same vehicle
    :param renavam: A string indicating the value of the vehicle's renavam
    :param appointment_date: The new appointment date for the rental you need create or update
    :param requested_days: A positive integer for represents the number of days required
    :param id_rental: If you need to validate an appointment update, you must provide the rental id for exclude it of
    the search
    :return: return True if the appointment not match other rentals or appointments and False otherwise
    """
    appointment_date = timezone.make_aware(datetime.strptime(str(appointment_date), '%Y-%m-%d'))
    # Check if there are any rentals with the allocation date within the new rental schedule plus X days
    initial_date = Q(
        Q(appointment_date__gte=appointment_date - timezone.timedelta(days=TOLERANCE_DAYS)),
        Q(appointment_date__lte=appointment_date + timezone.timedelta(days=requested_days + TOLERANCE_DAYS))
    )
    # Check if there are any rentals with the devolution date within the new rental schedule plus X days
    end_date = Q(
        Q(devolution_date_expected__gte=appointment_date - timezone.timedelta(days=TOLERANCE_DAYS)),
        Q(devolution_date_expected__lte=appointment_date + timezone.timedelta(days=requested_days + TOLERANCE_DAYS))
    )
    # Check if there are any rentals with a schedule tha overlaps with the new schedule
    other_date = Q(
        Q(appointment_date__lte=appointment_date - timezone.timedelta(days=TOLERANCE_DAYS)),
        Q(devolution_date_expected__gte=appointment_date + timezone.timedelta(days=requested_days + TOLERANCE_DAYS))
    )

    rentals = rental_models.Rental.objects.annotate(
        devolution_date_expected=RawSQL('DATE_ADD(appointment_date, INTERVAL requested_days DAY)', ()),
    )
    rentals = rentals.filter(Q(vehicle=renavam),
                             Q(status__in=('A', 'L')),
                             initial_date |
                             end_date |
                             other_date)

    if id_rental:
        return not rentals.exclude(id=id_rental)
    return not rentals


def additional_items_updated(rental_pk, additional_items_data) -> bool:
    """
    Check if additional items have been updated
    :param rental_pk: Get the primary key of the rental being updated
    :param additional_items_data: Get data for new rental additional items
    :return: Returns True if additional items have been updated, False otherwise
    """
    current_additional_items_data = rental_models.RentalAdditionalItem.objects.filter(rental=rental_pk)

    new_additional_items_data = {item['additional_item']: item['number'] for item in additional_items_data}
    # Check that the current number of items equal of the new number of items
    number_of_items = current_additional_items_data.count() == len(new_additional_items_data)
    # Check that both lists are the same
    is_present_and_equal_quantity = (current_item.additional_item in new_additional_items_data.keys() and
                                     current_item.number ==
                                     new_additional_items_data[current_item.additional_item]
                                     for current_item in current_additional_items_data)
    equal_lists = sum(is_present_and_equal_quantity) == current_additional_items_data.count()
    return not (number_of_items and equal_lists)

from rest_framework.utils import model_meta
from datetime import datetime, timedelta
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
    'A': ('vehicle_rental', 'insurance_rental', 'status_rental', 'appointment_date_rental', 'requested_days_rental',
          'rent_deposit_rental', 'driver_rental', 'additional_items_rental', 'additional_daily_cost_rental', ),
    'L': ('status_rental', 'driver_rental', ),
    'C': ('status_rental',),
    'D': ('status_rental', 'arrival_branch_rental', 'distance_branch_rental',),
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


def valid_appointment_update_or_cancellation(appointment_date) -> bool:
    """
    Verifies that the 3-day deadline for the schedule for updates and cancellations has been respected
    :param appointment_date: A string indicating the appointment date
    :return: A boolean indicating whether the appointment date minus 3 days is greater than today
    """
    return datetime.strptime(str(appointment_date), '%Y-%m-%d') - timedelta(days=3) > datetime.today()


def valid_rental_data_update(instance, validated_data) -> bool:
    """
    This validation verifies that only the allowed fields are updated, to ensure that the rest of the fields
    (autocomplete or post-completion) remain unchanged
    :param instance: An instance of the rental model class
    :param validated_data: A dictionary with the new values of the fields
    :return: Returns True if updates are accepted or False otherwise
    """
    status_rental = validated_data.get('status_rental')

    # Select the many to many fields
    info = model_meta.get_field_info(rental_models.Rental)
    many_to_many = list()
    for field_name, relation_info in info.relations.items():
        if relation_info.to_many and field_name not in ALLOW_FIELD_UPDATE[status_rental]:
            many_to_many.append(field_name)

    # Checks if the read-only fields have been modified
    disallow_field_update = validated_data.keys() - ALLOW_FIELD_UPDATE[status_rental]
    response = True

    for field in disallow_field_update:
        if field in many_to_many:
            equal_values = [client for client in instance.driver_rental.all()] == validated_data.get('driver_rental')
            if not equal_values:
                response = False
        else:
            if getattr(instance, field) != validated_data.get(field):
                response = False

    # TODO: Refatorar Trecho de código, pois alguns campos permitidos para alteração podem ser nulos
    # Checks if the fields have been filled
    # for field in ALLOW_FIELD_UPDATE[status_rental]:
    #     if not validated_data.get(field):
    #         response = False

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
    rented = Q(status_rental='L')
    # Check for scheduled rentals within the new rental schedule plus 3 days
    initial_date = Q(
        Q(status_rental__in=('A', 'L')),
        Q(appointment_date_rental__gte=timezone.now()),
        Q(appointment_date_rental__lte=timezone.now() + timezone.timedelta(days=requested_days + TOLERANCE_DAYS))
    )
    rentals = rental_models.Rental.objects.filter(
        Q(vehicle_rental=renavam_vehicle),
        rented |
        initial_date
    )

    if id_rental:
        return not rentals.exclude(id=id_rental)

    return not rentals


def valid_scheduled_vehicle(renavam_vehicle, appointment_date, requested_days, id_rental=None) -> bool:
    """
    Check that the appointment date coincides a rental or appointment for the same vehicle
    :param renavam_vehicle: A string indicating the value of the vehicle's renavam
    :param appointment_date: The new appointment date for the rental you need create or update
    :param requested_days: A positive integer for represents the number of days required
    :param id_rental: If you need to validate a appointment update, you must provide the rental id for exclude it of the
    search
    :return: return True if the appointment not match other rentals or appointments and False otherwise
    """
    appointment_date = timezone.make_aware(datetime.strptime(str(appointment_date), '%Y-%m-%d'))
    # Check if there are any rentals with the allocation date within the new rental schedule plus X days
    initial_date = Q(
        Q(appointment_date_rental__gte=appointment_date - timezone.timedelta(days=TOLERANCE_DAYS)),
        Q(appointment_date_rental__lte=appointment_date + timezone.timedelta(days=requested_days + TOLERANCE_DAYS))
    )
    # Check if there are any rentals with the devolution date within the new rental schedule plus X days
    end_date = Q(
        Q(devolution_date_expected__gte=(appointment_date - timezone.timedelta(days=TOLERANCE_DAYS))),
        Q(devolution_date_expected__lte=(appointment_date + timezone.timedelta(days=requested_days + TOLERANCE_DAYS)))
    )
    # Check if there are any rentals with a schedule tha overlaps with the new schedule
    other_date = Q(
        Q(appointment_date_rental__lte=appointment_date - timezone.timedelta(days=TOLERANCE_DAYS)),
        Q(devolution_date_expected__gte=(appointment_date + timezone.timedelta(days=requested_days + TOLERANCE_DAYS)))
    )

    rentals = rental_models.Rental.objects.annotate(
        devolution_date_expected=RawSQL('DATE_ADD(appointment_date_rental, INTERVAL requested_days_rental DAY)', ()),
    )
    rentals = rentals.filter(Q(vehicle_rental=renavam_vehicle),
                             Q(status_rental__in=('A', 'L')),
                             initial_date |
                             end_date |
                             other_date)

    if id_rental:
        return not rentals.exclude(id=id_rental)
    return not rentals

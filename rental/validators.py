from datetime import datetime, timedelta

STATUS_UPDATE = {
    'A': ('A', 'L', 'C'),
    'L': ('L', 'D',),
    'C': (),
    'D': (),
}


ALLOW_FIELD_UPDATE = {
    'A': ('vehicle_rental', 'insurance_rental', 'status_rental', 'appointment_date_rental',
          'requested_days_rental', 'rent_deposit_rental', 'additional_daily_cost_rental',
          'driver_rental', ),
    'L': ('status_rental', 'rent_date_rental', 'driver_rental', ),
    'C': ('status_rental', 'driver_rental', ),
    'D': ('status_rental', 'arrival_branch_rental', 'distance_branch_rental', 'driver_rental',),
}


def valid_status_rental_create(status_rental):
    """ Check the initial status allowed """
    return status_rental in ('A', 'L')


def valid_status_rental_update(old_status_rental, new_status_rental):
    """ Validates if the required status transition is allowed """
    return new_status_rental in STATUS_UPDATE[old_status_rental]


def valid_appointment_update_or_cancellation(appointment_date):
    """ Verifies that the 3-day deadline for the schedule for updates and cancellations has been respected """
    return datetime.strptime(str(appointment_date), '%Y-%m-%d') - timedelta(days=3) > datetime.today()


def valid_rental_data_update(instance, validated_data):
    """
        Validates if the required fields for the current status have been filled in and if the other fields remain empty
    """
    # Select the status rental
    status_rental = validated_data.get('status_rental')

    # Checks if the read-only fields have been modified
    disallow_field_update = validated_data.keys() - ALLOW_FIELD_UPDATE[status_rental]
    response = True
    for field in disallow_field_update:
        if getattr(instance, field) != validated_data.get(field):
            response = False
            print(field)

    # Checks if the fields have been filled
    for field in ALLOW_FIELD_UPDATE[validated_data.get('status_rental')]:
        if not validated_data.get(field):
            response = False
            print('a' + field)

    return response, ALLOW_FIELD_UPDATE[validated_data.get('status_rental')]

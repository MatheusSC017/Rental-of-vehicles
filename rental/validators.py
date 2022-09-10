from datetime import datetime, timedelta

STATUS_UPDATE = {
    'A': ('A', 'L', 'C'),
    'L': ('L', 'D', 'E'),
    'C': (),
    'D': (),
    'E': (),
}


ALLOW_FIELD_UPDATE = {
    'A': ('vehicle_rental', 'insurance_rental', 'status_rental', 'appointment_date_rental',
          'requested_days_rental', 'rent_deposit_rental', 'additional_daily_cost_rental',
          'driver_rental', ),
    'F': ('status_rental', 'fines_rental', 'driver_rental'),
    'L': ('status_rental', 'driver_rental', ),
    'C': (),
    'D': (),
    'E': (),
}


def valid_status_rental_create(status_rental):
    return status_rental in ('A', 'L')


def valid_status_rental_update(old_status_rental, new_status_rental):
    return new_status_rental in STATUS_UPDATE[old_status_rental]


def valid_appointment_update_or_cancellation(appointment_date):
    return datetime.strptime(str(appointment_date), '%Y-%m-%d') - timedelta(days=3) > datetime.today()


def valid_rental_data_update(instance, validated_data):
    status_rental = instance.status_rental \
        if instance.status_rental == 'A' and valid_appointment_update_or_cancellation(instance.appointment_date_rental)\
        else 'F'

    disallow_field_update = validated_data.keys() - ALLOW_FIELD_UPDATE[status_rental]
    response = True
    for field in disallow_field_update:
        if getattr(instance, field) != validated_data.get(field):
            response = False
    return response, ALLOW_FIELD_UPDATE[validated_data.get('status_rental')]

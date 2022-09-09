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
    'L': ('status_rental', 'driver_rental', ),
    'C': (),
    'D': (),
    'E': (),
}


def valid_status_rental(status_rental):
    return status_rental in ('A', 'L')


def valid_status_rental_update(old_status_rental, new_status_rental):
    return new_status_rental in STATUS_UPDATE[old_status_rental]


def valid_rental_data_update(instance, validated_data):
    disallow_field_update = validated_data.keys() - ALLOW_FIELD_UPDATE[validated_data.get('status_rental')]
    response = True
    for field in disallow_field_update:
        if instance.get(field) != validated_data.get(field):
            response = False
    return response, ALLOW_FIELD_UPDATE[validated_data.get('status_rental')]

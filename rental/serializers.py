from rest_framework.serializers import ModelSerializer, ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Insurance, AdditionalItems, Rental
from . import validators


class InsuranceSerializer(ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'


class AdditionalItemsSerializer(ModelSerializer):
    class Meta:
        model = AdditionalItems
        fields = '__all__'


class RentalSerializer(ModelSerializer):
    def create(self, validated_data):
        if not validators.valid_rental_states_on_create(validated_data.get('status_rental')):
            message = _('For rental registration, choose scheduled or rented only.')
            raise ValidationError(message)

        if validated_data.get('status_rental') == 'L':
            validated_data['appointment_date_rental'] = None
        else:
            if not validated_data['appointment_date_rental']:
                message = _('For vehicle scheduling, the scheduling date field is required.')
                raise ValidationError(message)

        validated_data['arrival_branch_rental'] = None
        validated_data['distance_branch_rental'] = None

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if not validators.valid_rental_states_on_update(instance.status_rental, validated_data.get('status_rental')):
            message = _('Required state transition is not valid.')
            raise ValidationError(message)

        valid_update, allowed_field = validators.valid_rental_data_update(instance, validated_data)
        if not valid_update:
            message = _(f'For the current state of the rental, only the following fields can be '
                        f'updated: {", ".join(allowed_field)}.')
            raise ValidationError(message)

        return super().update(instance, validated_data)

    class Meta:
        model = Rental
        fields = '__all__'
        read_only_fields = ['staff_rental', 'rent_date_rental', 'devolution_date_rental', 'actual_days_rental',
                            'fines_rental', 'daily_cost_rental', 'return_rate_rental', 'total_cost_rental',
                            'outlet_branch_rental', ]

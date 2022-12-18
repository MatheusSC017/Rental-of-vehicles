from rest_framework.serializers import ModelSerializer, ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Insurance, AdditionalItems, Rental, RentalAdditionalItem
from . import validators


class InsuranceSerializer(ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'


class AdditionalItemsSerializer(ModelSerializer):
    class Meta:
        model = AdditionalItems
        fields = '__all__'


class RentalAdditionalItemSerializer(ModelSerializer):
    class Meta:
        model = RentalAdditionalItem
        fields = '__all__'
        read_only_fields = ['rental_relationship', ]


class RentalSerializer(ModelSerializer):
    error_messages_rental = {
        'invalid_status_creation': _('For rental registration, choose scheduled or rented only.'),
        'invalid_scheduled_date': _('For vehicle scheduling, a valid scheduling date field is required.'),
        'vehicle_already_scheduled': _('The chosen vehicle is already rented or there is '
                                       'an appointment scheduled for it.'),
        'invalid_status_transition': _('Required state transition is not valid.'),
        'invalid_field_update': _('For the current state of the rental, only the following fields can be updated: '),
    }

    additional_items_rental = RentalAdditionalItemSerializer(many=True)

    class Meta:
        model = Rental
        fields = '__all__'
        read_only_fields = ['staff_rental', 'rent_date_rental', 'devolution_date_rental', 'actual_days_rental',
                            'fines_rental', 'daily_cost_rental', 'return_rate_rental', 'total_cost_rental',
                            'outlet_branch_rental', 'additional_daily_cost_rental']

    def create(self, validated_data):
        if not validators.valid_rental_states_on_create(validated_data.get('status_rental')):
            raise ValidationError(self.error_messages_rental.get('invalid_status_creation'))

        if validated_data.get('status_rental') == 'L':
            validated_data['appointment_date_rental'] = None

            if not validators.valid_rented_vehicle(validated_data.get('vehicle_rental'),
                                                   validated_data.get('requested_days_rental')):
                raise ValidationError(self.error_messages_rental.get('vehicle_already_scheduled'))
        else:
            if not validators.valid_appointment_creation(validated_data.get('appointment_date_rental')):
                raise ValidationError(self.error_messages_rental.get('invalid_scheduled_date'))

            if not validators.valid_scheduled_vehicle(validated_data.get('vehicle_rental'),
                                                      validated_data.get('appointment_date_rental'),
                                                      validated_data.get('requested_days_rental')):
                raise ValidationError(self.error_messages_rental.get('vehicle_already_scheduled'))

        validated_data['arrival_branch_rental'] = None
        validated_data['distance_branch_rental'] = None

        additional_items_data = validated_data.pop('additional_items_rental')
        rental = super().create(validated_data)
        for additional_item in additional_items_data:
            RentalAdditionalItem.objects.create(rental_relationship=rental, **additional_item)
        return rental

    def update(self, instance, validated_data):
        additional_items_data = validated_data.pop('additional_items_rental')

        if not validators.valid_rental_states_on_update(instance.status_rental, validated_data.get('status_rental')):
            raise ValidationError(self.error_messages_rental.get('invalid_status_transition'))

        valid_update, allowed_field = validators.valid_rental_data_update(instance, validated_data)
        if not valid_update:
            raise ValidationError(self.error_messages_rental.get('invalid_field_update') + ", ".join(allowed_field))

        if validated_data.get('status_rental') == 'A':
            if not validators.valid_scheduled_vehicle(validated_data.get('vehicle_rental'),
                                                      validated_data.get('appointment_date_rental'),
                                                      validated_data.get('requested_days_rental'),
                                                      instance.pk):
                raise ValidationError(self.error_messages_rental.get('vehicle_already_scheduled'))

        if validated_data.get('status_rental') == 'L':
            if not validators.valid_rented_vehicle(validated_data.get('vehicle_rental'),
                                                   validated_data.get('requested_days_rental'),
                                                   instance.pk):
                raise ValidationError(self.error_messages_rental.get('vehicle_already_scheduled'))

        current_additional_items_data = RentalAdditionalItem.objects.filter(rental_relationship=instance.pk)
        new_additional_items_data = [item['additional_item_relationship'] for item in additional_items_data]

        # The next step will be to update the relationship between additional item and rent
        for current_item in current_additional_items_data:
            # If the current additional item is not present in the list of new additional items, it must be deleted
            if current_item.additional_item_relationship not in new_additional_items_data:
                current_item.delete()
            # if it is present in the list of additional new items, the quantity value must be updated
            else:
                new_data = [item for item in additional_items_data if item['additional_item_relationship'] ==
                            current_item.additional_item_relationship][0]
                # The code in the line below deletes the updated record from the list of additional new items
                additional_items_data = [item for item in additional_items_data if item['additional_item_relationship']
                                         != current_item.additional_item_relationship]
                current_item.number_relationship = new_data['number_relationship']
                current_item.save()
        # The last step will be create new relationships for rent and additional items
        for additional_item in additional_items_data:
            RentalAdditionalItem.objects.create(rental_relationship=instance, **additional_item)

        return super().update(instance, validated_data)

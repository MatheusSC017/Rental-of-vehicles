import requests
from json import loads
from requests import RequestException
from dotenv import load_dotenv
from rest_framework.serializers import ModelSerializer, ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from .models import Insurance, AdditionalItems, Rental, RentalAdditionalItem
from . import validators


load_dotenv()


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
        read_only_fields = ['rental', ]


class RentalSerializer(ModelSerializer):
    rental_error_messages = {
        'invalid_status_creation': _('For rental registration, choose scheduled or rented only.'),
        'invalid_scheduled_date': _('For vehicle scheduling, a valid scheduling date field is required.'),
        'vehicle_already_scheduled': _('The chosen vehicle is already rented or there is '
                                       'an appointment scheduled for it.'),
        'invalid_status_transition': _('Required state transition is not valid.'),
        'invalid_field_update': _('For the current state of the rental, only the following fields can be updated: '),
        'invalid_additional_items_updated': _('For the current rental status, additional items cannot be changed'),
        'invalid_additional_item_order': _('Order number for additional item is greater than stock'),
        'invalid_branch': _('The additional item must belong to the same branch where the vehicle was picked up.'),
        'invalid_staff': _('The employee is not assigned to the branch where the vehicle is located'),
    }

    additional_items = RentalAdditionalItemSerializer(many=True)

    class Meta:
        model = Rental
        fields = [
            'id', 'vehicle', 'insurance', 'staff', 'client', 'status', 'outlet_branch', 'arrival_branch',
            'distance_branch', 'appointment_date', 'rent_date', 'devolution_date', 'requested_days', 'actual_days',
            'fines', 'rent_deposit', 'daily_cost', 'additional_daily_cost', 'return_rate', 'total_cost', 'driver',
            'additional_items'
        ]
        read_only_fields = ['staff', 'rent_date', 'devolution_date', 'actual_days', 'fines', 'daily_cost',
                            'return_rate', 'total_cost', 'outlet_branch', 'additional_daily_cost']

    def validate(self, attrs):
        """ Validate the attributes
        Check if the chosen additional items belong to the same branch as the vehicle
        :param attrs: get an instance of collections.OrderedDict with the attributes
        :return: return an instance of collections.OrderedDict with the attributes
        """
        for item in attrs['additional_items']:
            if item['additional_item'].branch != attrs['vehicle'].branch:
                raise ValidationError(self.rental_error_messages.get('invalid_branch'))
        return attrs

    @transaction.atomic
    def create(self, validated_data) -> Rental:
        """
        This function will be applying the necessary validations to verify if the create request is valid
        :param validated_data: The data for create an instance of the Rental model class
        :return: An instance of the Rental model class
        """
        if not validators.valid_rental_states_on_create(validated_data.get('status')):
            raise ValidationError(self.rental_error_messages.get('invalid_status_creation'))

        if validated_data['vehicle'].branch.pk != validated_data['staff'].branch.pk:
            raise ValidationError(self.rental_error_messages.get('invalid_staff'))

        if validated_data.get('status') == 'L':
            validated_data['appointment_date'] = None

            if not validators.valid_rented_vehicle(validated_data.get('vehicle'),
                                                   validated_data.get('requested_days')):
                raise ValidationError(self.rental_error_messages.get('vehicle_already_scheduled'))
        else:
            if not validators.valid_appointment_creation(validated_data.get('appointment_date')):
                raise ValidationError(self.rental_error_messages.get('invalid_scheduled_date'))

            if not validators.valid_scheduled_vehicle(validated_data.get('vehicle'),
                                                      validated_data.get('appointment_date'),
                                                      validated_data.get('requested_days')):
                raise ValidationError(self.rental_error_messages.get('vehicle_already_scheduled'))

        validated_data['arrival_branch'] = None
        validated_data['distance_branch'] = None

        additional_items_data = validated_data.pop('additional_items')
        rental = super().create(validated_data)
        self._create_additional_items_relationship(rental, additional_items_data)
        return rental

    @transaction.atomic
    def update(self, instance, validated_data) -> Rental:
        """
        This function will be applying the necessary validations to verify if the update request is valid
        :param instance: An instance of the Rental model class
        :param validated_data: The new data for the instance of the Rental model class
        :return: An instance of the Rental model class with the new data
        """

        additional_items_data = validated_data.pop('additional_items')

        if validated_data['vehicle'].branch.pk != validated_data['staff'].branch.pk:
            raise ValidationError(self.rental_error_messages.get('invalid_staff'))

        if not validators.valid_rental_states_on_update(instance.status, validated_data.get('status')):
            raise ValidationError(self.rental_error_messages.get('invalid_status_transition'))

        valid_update, allowed_field = validators.valid_rental_data_update(instance, validated_data)
        if not valid_update:
            raise ValidationError(self.rental_error_messages.get('invalid_field_update') + ", ".join(allowed_field))

        if validated_data.get('status') in ('A', 'L',):
            if validated_data.get('status') == 'A':
                if not validators.valid_scheduled_vehicle(validated_data.get('vehicle'),
                                                          validated_data.get('appointment_date'),
                                                          validated_data.get('requested_days'),
                                                          instance.pk):
                    raise ValidationError(self.rental_error_messages.get('vehicle_already_scheduled'))

            if validated_data.get('status') == 'L':
                if not validators.valid_rented_vehicle(validated_data.get('vehicle'),
                                                       validated_data.get('requested_days'),
                                                       instance.pk):
                    raise ValidationError(self.rental_error_messages.get('vehicle_already_scheduled'))

                if validators.additional_items_updated(instance.pk, additional_items_data):
                    raise ValidationError(self.rental_error_messages.get('invalid_additional_items_updated'))

            self._update_additional_items_relationship(instance, additional_items_data)
        else:
            # Coordinate API to calculate the distance
            if validated_data.get('arrival_branch'):
                try:
                    start_address = validated_data['outlet_branch'].address
                    end_address = validated_data['arrival_branch'].address
                    data = {
                        "start_address": {
                            "street": start_address.street,
                            "number": start_address.number,
                            "district": start_address.district,
                            "city": start_address.city,
                            "state": start_address.state,
                            "country": "Brasil"
                        },
                        "end_address": {
                            "street": end_address.street,
                            "number": end_address.number,
                            "district": end_address.district,
                            "city": end_address.city,
                            "state": end_address.state,
                            "country": "Brasil"
                        }
                    }
                    headers = {"token": settings.COORDINATES_API_KEY}
                    response = requests.get(settings.COORDINATES_URL, json=data, headers=headers)
                    validated_data['distance_branch'] = loads(response.content)['distance'] / 1000
                except (RequestException, ConnectionError):
                    validated_data['distance_branch'] = 0
            self._inventory_update_for_rental_devolution_or_cancellation(instance)

        return super().update(instance, validated_data)

    def _update_additional_items_relationship(self, rental, additional_items_data) -> None:
        """
        This function will be to update the relationship between additional item and rent
        :param rental: Get an instance of the Rental model class
        :param additional_items_data: Get data for new rental additional items
        :return: None
        """
        new_additional_items_data = [item['additional_item'] for item in additional_items_data]

        for current_item in rental.additional_items.all():
            # If the current additional item is not present in the list of new additional items, it must be deleted
            if current_item.additional_item not in new_additional_items_data:
                self._update_stock_additional_items(additional_item=current_item.additional_item,
                                                    old_items_number=current_item.number)
                current_item.delete()
            # if it is present in the list of additional new items, the quantity value must be updated
            else:
                new_data = [item for item in additional_items_data if item['additional_item'] ==
                            current_item.additional_item][0]
                # The code in the line below deletes the updated record from the list of additional new items
                additional_items_data = [item for item in additional_items_data if item['additional_item']
                                         != current_item.additional_item]

                self._update_stock_additional_items(additional_item=current_item.additional_item,
                                                    items_number=new_data['number'],
                                                    old_items_number=current_item.number)

                current_item.number = new_data['number']
                current_item.save()

        # The last step will be to create new relationships for rent and additional items
        self._create_additional_items_relationship(rental, additional_items_data)

    def _create_additional_items_relationship(self, rental, additional_items_data) -> None:
        """
        This function will be to create the relationship between additional item and rent
        :param rental: Get an instance of the Rental model class
        :param additional_items_data: Get data for create rental additional items
        :return: None
        """
        for additional_item in additional_items_data:
            self._update_stock_additional_items(additional_item=additional_item['additional_item'],
                                                items_number=additional_item['number'])
            RentalAdditionalItem.objects.create(rental=rental, **additional_item)

    def _inventory_update_for_rental_devolution_or_cancellation(self, rental) -> None:
        """
        This function will be used to update the stock when there is a devolution or cancellation of the rent
        :param rental: Get an instance of the Rental model class
        :return: None
        """
        for item in rental.additional_items.all():
            self._update_stock_additional_items(additional_item=item.additional_item,
                                                old_items_number=item.number)

    def _update_stock_additional_items(self, additional_item, items_number=0, old_items_number=0):
        """
        This function will be used to update the stock of an additional item
        :param additional_item: Get an instance of the AdditionalItem model class
        :param items_number: Gets the new amount of items that will be rented
        :param old_items_number: Gets the old amount of items that was being rented
        :return: None
        """
        additional_item.stock = additional_item.stock - items_number + old_items_number
        if additional_item.stock < 0:
            raise ValidationError(self.rental_error_messages.get('invalid_additional_item_order'))
        additional_item.save()

from rest_framework.serializers import ModelSerializer
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from .models import Insurance, AdditionalItems, Rental
from .utils import *
from . import validators


class InsuranceSerializer(ModelSerializer):
    class Meta:
        model = Insurance
        fields = ['id', 'title', 'coverage', 'price', ]


class AdditionalItemsSerializer(ModelSerializer):
    class Meta:
        model = AdditionalItems
        fields = ['id', 'name', 'daily_cost', 'stock', 'branch', ]


class RentalAdditionalItemSerializer(ModelSerializer):
    class Meta:
        model = RentalAdditionalItem
        fields = '__all__'
        read_only_fields = ['rental', ]


class RentalSerializer(ModelSerializer):
    additional_items = RentalAdditionalItemSerializer(many=True)

    class Meta:
        model = Rental
        fields = [
            'id', 'vehicle', 'insurance', 'staff', 'client', 'status', 'outlet_branch', 'arrival_branch',
            'distance_branch', 'appointment_date', 'rent_date', 'devolution_date', 'requested_days', 'actual_days',
            'fines', 'rent_deposit', 'daily_cost', 'additional_daily_cost', 'return_rate', 'total_cost', 'driver',
            'additional_items'
        ]


class GenericRentalCreateSerializer(ModelSerializer):
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


class AppointmentSerializer(GenericRentalCreateSerializer):
    class Meta:
        model = Rental
        fields = [
            'vehicle', 'insurance', 'client', 'status', 'appointment_date', 'requested_days', 'rent_deposit', 'driver',
            'additional_items', 'staff'
        ]
        read_only_fields = [
            'status', 'staff'
        ]

    def validate_appointment(self, validated_data, rental_id=None):
        if validated_data['vehicle'].branch.pk != validated_data['staff'].branch.pk:
            raise ValidationError(self.rental_error_messages.get('invalid_staff'))

        if not validators.valid_appointment_creation(validated_data.get('appointment_date')):
            raise ValidationError(self.rental_error_messages.get('invalid_scheduled_date'))

        if not validators.valid_scheduled_vehicle(validated_data.get('vehicle'),
                                                  validated_data.get('appointment_date'),
                                                  validated_data.get('requested_days'),
                                                  rental_id):
            raise ValidationError(self.rental_error_messages.get('vehicle_already_scheduled'))

    @transaction.atomic
    def create(self, validated_data) -> Rental:
        """
        This function will be applying the necessary validations to verify if the create request is valid
        :param validated_data: The data for create an instance of the Rental model class
        :return: An instance of the Rental model class
        """
        validated_data['status'] = 'A'

        self.validate_appointment(validated_data)

        additional_items_data = validated_data.pop('additional_items')
        rental = super().create(validated_data)
        create_additional_items_relationship(rental, additional_items_data)
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
        self.validate_appointment(validated_data, rental_id=instance.pk)

        update_additional_items_relationship(instance, additional_items_data)

        return super().update(instance, validated_data)


class RentCreateSerializer(GenericRentalCreateSerializer):
    class Meta:
        model = Rental
        fields = [
            'vehicle', 'insurance', 'client', 'status', 'requested_days', 'rent_deposit', 'driver', 'additional_items'
        ]
        read_only_fields = [
            'status'
        ]

    @transaction.atomic
    def create(self, validated_data) -> Rental:
        """
        This function will be applying the necessary validations to verify if the create request is valid
        :param validated_data: The data for create an instance of the Rental model class
        :return: An instance of the Rental model class
        """

        validated_data['status'] = 'L'

        if not validators.valid_rented_vehicle(validated_data.get('vehicle'), validated_data.get('requested_days')):
            raise ValidationError(self.rental_error_messages.get('vehicle_already_scheduled'))

        additional_items_data = validated_data.pop('additional_items')
        rental = super().create(validated_data)
        create_additional_items_relationship(rental, additional_items_data)
        return rental


class RentUpdateSerializer(ModelSerializer):
    additional_items = RentalAdditionalItemSerializer(many=True, read_only=True)

    class Meta:
        model = Rental
        fields = [
            'vehicle', 'insurance', 'client', 'status', 'requested_days', 'rent_deposit', 'driver', 'additional_items'
        ]
        read_only_fields = [
            'vehicle', 'insurance', 'client', 'status', 'requested_days', 'rent_deposit', 'additional_items'
        ]

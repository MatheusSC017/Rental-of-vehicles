from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Insurance, Rental
from . import validators


class InsuranceSerializer(ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'


class RentalSerializer(ModelSerializer):
    def create(self, validated_data):
        if not validators.valid_status_rental_create(validated_data.get('status_rental')):
            raise ValidationError('Para cadastro de alocação informe como opção Agendado ou Alugado somente.')

        if validated_data.get('status_rental') == 'L':
            validated_data['appointment_date_rental'] = None

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if not validators.valid_status_rental_update(instance.status_rental, validated_data.get('status_rental')):
            raise ValidationError('A transição de status requirida não é válida.')

        valid_update, allowed_field = validators.valid_rental_data_update(instance, validated_data)
        if not valid_update:
            raise ValidationError('O estado que o veiculo se encontra só permite que os seguintes campos sejam '
                                  f'alterados: {", ".join(allowed_field)}.')

        return super().update(instance, validated_data)

    class Meta:
        model = Rental
        fields = '__all__'
        read_only_fields = ['staff_rental', 'rent_date_rental', 'devolution_date_rental', 'actual_days_rental',
                            'fines_rental', 'daily_cost_rental', 'return_rate_rental', 'total_cost_rental',
                            'outlet_branch_rental', 'arrival_branch_rental']

from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Insurance, Rental
from .validators import valid_status_rental


class InsuranceSerializer(ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'


class RentalSerializer(ModelSerializer):
    def create(self, validated_data):
        if not valid_status_rental(validated_data.get('status_rental')):
            raise ValidationError('Para cadastro de alocação informe como opção Agendado ou Alugado somente.')
        if validated_data.get('status_rental') == 'L':
            validated_data['appointment_date_rental'] = None
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.status_rental == 'A' and validated_data.get('status_rental') not in ('A', 'L', 'C'):
            raise ValidationError('Um carro agendado somente pode transitar para o estado Alocado e Cancelado.')
        return super().update(instance, validated_data)

    class Meta:
        model = Rental
        fields = '__all__'
        read_only_fields = ['staff_rental', 'rent_date_rental', 'devolution_date_rental', 'actual_days_rental',
                            'fines_rental', 'daily_cost_rental', 'return_rate_rental', 'total_cost_rental',
                            'arrival_branch_rental']

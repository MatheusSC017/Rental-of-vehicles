from rest_framework.serializers import ModelSerializer
from .models import Insurance, Rental


class InsuranceSerializer(ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'


class RentalSerializer(ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'
        read_only_fields = ['staff_rental', 'devolution_date_rental', 'actual_deadline_rental', 'fines_rental',
                            'daily_cost_rental', 'return_rate_rental', 'total_cost_rental', 'arrival_branch_rental']

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

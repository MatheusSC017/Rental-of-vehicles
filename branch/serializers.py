from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import Branch


class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

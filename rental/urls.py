from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InsuranceViewSet, RentalViewSet

router = DefaultRouter()
router.register('seguros', InsuranceViewSet)
router.register('', RentalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

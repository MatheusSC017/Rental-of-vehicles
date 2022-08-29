from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BranchViewSet, BranchAddressViewSet, BranchVehicleViewSet

router = DefaultRouter()
router.register('enderecos', BranchAddressViewSet)
router.register('(?P<branch>[^/.]+)/veiculos', BranchVehicleViewSet)
router.register('', BranchViewSet)

urlpatterns = [
    path('', include(router.urls))
]

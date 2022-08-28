from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BranchViewSet, BranchAddressViewSet

router = DefaultRouter()
router.register('enderecos', BranchAddressViewSet)
router.register('', BranchViewSet)

urlpatterns = [
    path('', include(router.urls))
]

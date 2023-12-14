"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rental.views import InsuranceViewSet, AdditionalItemsViewSet, RentalViewSet, late_appointments, late_devolutions
from address.views import AddressViewSet
from branch.views import BranchViewSet, BranchAddressViewSet, BranchVehicleViewSet
from client.views import ClientViewSet, UserViewSet
from vehicle.views import VehicleViewSet, VehicleClassificationViewSet

router_root = DefaultRouter()
router_root.register('insurances', InsuranceViewSet, 'Insurances')
router_root.register('additional_items', AdditionalItemsViewSet, 'AdditionalItems')
router_root.register('rents', RentalViewSet, 'Rentals')
router_root.register('addresses', AddressViewSet, 'Addresses')
router_root.register('branches', BranchViewSet, 'Branches')
router_root.register('customers/users', UserViewSet, 'Users')
router_root.register('customers', ClientViewSet, 'Clients')
router_root.register('vehicles', VehicleViewSet, 'Vehicles')
router_root.register('classifications', VehicleClassificationViewSet, 'Classifications')

router_branches = DefaultRouter()
router_branches.register('addresses', BranchAddressViewSet, 'BranchAddresses')
router_branches.register('vehicles', BranchVehicleViewSet, 'BranchVehicles')

urlpatterns = [
    path('', include(router_root.urls)),
    path('branches/<int:pk>/', include(router_branches.urls)),
    path('rents/expired_appointments', late_appointments),
    path('rents/expired_returns', late_devolutions),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

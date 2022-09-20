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
from rest_framework.routers import DefaultRouter
from rental.views import InsuranceViewSet, AdditionalItemsViewSet, RentalViewSet
from address.views import AddressViewSet
from branch.views import BranchViewSet, BranchAddressViewSet, BranchVehicleViewSet
from client.views import ClientViewSet, UserViewSet
from vehicle.views import VehicleViewSet

router = DefaultRouter()
router.register('seguros', InsuranceViewSet)
router.register('itens_adicionais', AdditionalItemsViewSet)
router.register('alugueis', RentalViewSet)
router.register('enderecos', AddressViewSet)
router.register('filiais', BranchViewSet)
# router.register('filiais/enderecos', BranchAddressViewSet)
# router.register('filial-veiculos', BranchVehicleViewSet, 'filiais/<int:pk>/veiculos')
router.register('clientes/usuarios', UserViewSet)
router.register('clientes', ClientViewSet)
router.register('veiculos', VehicleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]

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
router_root.register('seguros', InsuranceViewSet, 'Insurances')
router_root.register('itens_adicionais', AdditionalItemsViewSet, 'AdditionalItems')
router_root.register('alugueis', RentalViewSet, 'Rentals')
router_root.register('enderecos', AddressViewSet, 'Addresses')
router_root.register('filiais', BranchViewSet, 'Branches')
router_root.register('clientes/usuarios', UserViewSet, 'Users')
router_root.register('clientes', ClientViewSet, 'Clients')
router_root.register('veiculos', VehicleViewSet, 'Vehicles')
router_root.register('classificacoes', VehicleClassificationViewSet, 'Classifications')

router_branches = DefaultRouter()
router_branches.register('endereco', BranchAddressViewSet, 'BranchAddresses')
router_branches.register('veiculos', BranchVehicleViewSet, 'BranchVehicles')

urlpatterns = [
    path('', include(router_root.urls)),
    path('filiais/<int:pk>/', include(router_branches.urls)),
    path('alugueis/agendamentos_vencidos', late_appointments),
    path('alugueis/devolucoes_vencidas', late_devolutions),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
from rental.views import InsuranceViewSet, AdditionalItemsViewSet, RentalViewSet
from address.views import AddressViewSet
from branch.views import BranchViewSet, BranchAddressViewSet, BranchVehicleViewSet
from client.views import ClientViewSet, UserViewSet
from vehicle.views import VehicleViewSet

router = DefaultRouter()
router.register('seguros', InsuranceViewSet, 'seguros')
router.register('itens_adicionais', AdditionalItemsViewSet, 'itens_adicionais')
router.register('alugueis', RentalViewSet, 'alugueis')
router.register('enderecos', AddressViewSet, 'enderecos')
router.register('filiais', BranchViewSet, 'filiais')
router.register('clientes/usuarios', UserViewSet, 'usuarios')
router.register('clientes', ClientViewSet, 'clientes')
router.register('veiculos', VehicleViewSet, 'veiculos')

urlpatterns = [
    path('', include(router.urls)),
    path('filiais/<int:pk>/endereco/', BranchAddressViewSet.as_view()),
    path('filiais/<int:pk>/veiculos/', BranchVehicleViewSet.as_view()),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

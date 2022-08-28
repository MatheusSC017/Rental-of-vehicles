from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, UserViewSet

router = DefaultRouter()
router.register('usuarios', UserViewSet)
router.register('', ClientViewSet)

urlpatterns = [
    path('', include(router.urls))
]

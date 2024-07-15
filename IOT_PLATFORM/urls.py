from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'company', views.CompanyViewSet)
router.register(r'location', views.LocationViewSet)
router.register(r'sensor', views.SensorViewSet)
router.register(r'sensor-data', views.SensorDataViewSet, basename='sensordata')

urlpatterns = [
    path('', include(router.urls)),
]

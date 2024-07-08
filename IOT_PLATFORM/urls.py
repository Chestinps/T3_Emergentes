from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('admin', views.AdminView)
router.register('company', views.CompanyView)
router.register('location', views.LocationView)
router.register('sensor', views.SensorView)

urlpatterns = [
    path('t3/', include(router.urls))
]
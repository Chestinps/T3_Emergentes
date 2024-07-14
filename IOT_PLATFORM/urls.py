from django.urls import path, include
from .views import RegistrationView
from .views import LoginView
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('admin', views.AdminView)
router.register('company', views.CompanyView)
router.register('location', views.LocationView)
router.register('sensor', views.SensorView)
router.register('sensor-data', views.SensorDataView)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('user/', views.UserView.as_view()),
]
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AdminSerializer, CompanySerializer, LocationSerializer, SensorSerializer
from .models import Admin, Company, Location, Sensor

# Create your views here.

class AdminView(viewsets.ModelViewSet):
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()

class CompanyView(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

class LocationView(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

class SensorView(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()

    

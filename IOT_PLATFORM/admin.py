from django.contrib import admin
from .models import Admin, Company, Location, Sensor, SensorData

# Register your models here.
admin.site.register(Admin)
admin.site.register(Company)
admin.site.register(Location)
admin.site.register(Sensor)
admin.site.register(SensorData)


from django.db import models

# Create your models here.

class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Company(models.Model):
    ID = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    company_api_key = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

class Location(models.Model):
    ID = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=100)
    location_country = models.CharField(max_length=100)
    location_city = models.CharField(max_length=100)
    location_meta = models.CharField(max_length=100)

    def __str__(self):
        return self.location_name

class Sensor(models.Model):
    ID = models.AutoField(primary_key=True)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    sensor_name = models.CharField(max_length=100)
    sensor_category = models.CharField(max_length=100)
    sensor_meta = models.CharField(max_length=100)
    sensor_api_key = models.CharField(max_length=100)

    def __str__(self):
        return self.sensor_name

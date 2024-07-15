from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Company, Sensor

class CompanyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Company-Api-Key')
        if not api_key:
            return None

        try:
            company = Company.objects.get(company_api_key=api_key)
            return (company, None)
        except Company.DoesNotExist:
            return None

class SensorAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Sensor-Api-Key')
        if not api_key:
            return None

        try:
            sensor = Sensor.objects.get(sensor_api_key=api_key)
        except Sensor.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')

        return (sensor, None)

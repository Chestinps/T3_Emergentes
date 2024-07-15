from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Company, Location, Sensor, SensorData
from .serializers import LocationSerializer, SensorSerializer, SensorDataSerializer, CompanySerializer
from .authentication import CompanyAuthentication, SensorAuthentication
from .permissions import IsCompanyAuthenticated
from rest_framework.permissions import AllowAny
from datetime import datetime


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Company.objects.all()


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    authentication_classes = [CompanyAuthentication]
    permission_classes = [IsCompanyAuthenticated]

    def get_queryset(self):
        return Location.objects.filter(company_id=self.request.user)

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    authentication_classes = [CompanyAuthentication]
    permission_classes = [IsCompanyAuthenticated]

    def get_queryset(self):
        return Sensor.objects.filter(location_id__company_id=self.request.user)
    
class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
    authentication_classes = [SensorAuthentication]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        api_key = request.headers.get('Sensor-Api-Key')
        if not api_key:
            return Response({'detail': 'Sensor-Api-Key header is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sensor = Sensor.objects.get(sensor_api_key=api_key)
        except Sensor.DoesNotExist:
            return Response({'detail': 'Invalid API key'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['sensor_id'] = sensor.ID  # Ajusta aquí para usar ID
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def query(self, request):
        from_timestamp = request.query_params.get('from')
        to_timestamp = request.query_params.get('to')
        sensor_ids = request.query_params.getlist('sensor_id')

        # Verifica si los timestamps están presentes y en formato correcto
        if not from_timestamp or not to_timestamp:
            return Response({'detail': 'Required parameters: from, to'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Intenta convertir los timestamps a objetos datetime
            from_timestamp = datetime.fromisoformat(from_timestamp)
            to_timestamp = datetime.fromisoformat(to_timestamp)
        except ValueError:
            return Response({'detail': 'Invalid timestamp format'}, status=status.HTTP_400_BAD_REQUEST)

        # Filtra los datos de SensorData según los parámetros
        queryset = self.get_queryset().filter(
            sensor_id__in=sensor_ids,
            sensor_data_time__gte=from_timestamp,
            sensor_data_time__lte=to_timestamp
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# yourapp/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Company, Location, Sensor, SensorData
from .serializers import LocationSerializer, SensorSerializer, SensorDataSerializer
from .authentication import CompanyAuthentication
from .permissions import IsCompanyAuthenticated  # Import your custom permission class

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    authentication_classes = [CompanyAuthentication]
    permission_classes = [IsCompanyAuthenticated]  # Use your custom permission class

    def get_queryset(self):
        return Location.objects.filter(company_id=self.request.user)

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    authentication_classes = [CompanyAuthentication]
    permission_classes = [IsCompanyAuthenticated]  # Use your custom permission class

    def get_queryset(self):
        return Sensor.objects.filter(location_id__company_id=self.request.user)

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

    def create(self, request, *args, **kwargs):
        api_key = request.headers.get('Sensor-Api-Key')
        if not api_key:
            return Response({'detail': 'Sensor-Api-Key header is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sensor = Sensor.objects.get(sensor_api_key=api_key)
        except Sensor.DoesNotExist:
            return Response({'detail': 'Invalid API key'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['sensor_id'] = sensor.id
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def query(self, request):
        from_timestamp = request.query_params.get('from')
        to_timestamp = request.query_params.get('to')
        sensor_ids = request.query_params.getlist('sensor_id')
        
        if not from_timestamp or not to_timestamp or not sensor_ids:
            return Response({'detail': 'Required parameters: from, to, sensor_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from_timestamp = int(from_timestamp)
            to_timestamp = int(to_timestamp)
        except ValueError:
            return Response({'detail': 'Invalid timestamp format'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(
            sensor_id__in=sensor_ids,
            sensor_data_time__gte=from_timestamp,
            sensor_data_time__lte=to_timestamp
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
